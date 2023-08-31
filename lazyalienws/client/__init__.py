from mcdreforged.api.decorator import new_thread
from mcdreforged.api.types import ServerInterface
from lazyalienws.constants.core_constants import NAME
import websocket, time, threading, re
from typing import Self

class MCDR_velocity_plugin:

    def __init__(self, server:ServerInterface, url:str, client_name:str) -> None:
        if client_name == None:
            server.logger.info("Change the client name in config.")
            server.say(f"§e[{NAME}] §c终止§f: §4必须在配置文件中设置客户端名称")
        else:
            server.logger.info(server)
            try:
                self.ws = MCDR_WebSocketClient(server, url, client_name)
                self.ws.start()
            except Exception as e:
                server.logger.warn(e)
    
    def on_info(self, server, info):
        content = info.content
        if content[:3] in ["[+]","[-]"]:
            self.ws.send_message(content[4:])
    
    def on_unload(self, server):
        self.ws.end()

class MCDR_plugin:

    def __init__(self, server:ServerInterface, url:str, client_name:str) -> None:
        if client_name == None:
            server.logger.info("Change the client name in config.")
            server.say(f"§e[{NAME}] §c终止§f: §4必须在配置文件中设置客户端名称")
        else:
            server.logger.info(server)
            try:
                self.ws = MCDR_WebSocketClient(server, url, client_name)
                self.ws.start()
            except Exception as e:
                server.logger.warn(e)
    
    def on_user_info(self, server, info):
        if info.player != None:
            try:
                if info.content[0] == "#":
                    self.ws.send_message("<%s> %s"%(info.player, info.content))
                    self.ws.send_command(info.player, info.content)
                else:
                    self.ws.send_message("<%s> %s"%(info.player, info.content))
            except websocket._exceptions.WebSocketConnectionClosedException as e:
                ...
    
    def on_info(self, server, info):
        if not info.is_player:
            self.ws.on_info(info)
    
    def on_player_joined(self, server, player, info):
        re_result = re.match(r"(?:\[\w+\])?\w+\[([local0-9.]+)] logged in", info)
        if re_result:
            ip = re_result.groups()[0]
        server.logger.info(f'player:{player}, ip:{ip}, action:logged')
        if ip != "local":
            self.ws.send_command(player, "#LAS")
    
    def on_player_left(self, server, player):
        pass
    
    def on_unload(self, server):
        self.ws.end()
    
    def on_server_startup(self, server):
        self.ws.send_message('Server Started')

    def on_server_stop(self, server, server_return_code):
        self.ws.send_message('Server Stoped: %s'%server_return_code)


class MCDR_WebSocketClient:

    # 单例
    _singleton = None
    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._singleton:
            cls._singleton = object.__new__(cls)
        return cls._singleton

    def __init__(self, server, url: str, client_name: str, debug: bool = False) -> None:
        self.url = url
        self.client_name = client_name
        self.ws = None
        self.debug = debug
        self.logger = server.logger
        self.server = server
        self.request_api = {}
        self.is_running = True

    def on_open(self, client):

        self.logger.info("Connected")

        MESSAGE = {"client": self.client_name, "action": "Connection", "value": "Connected"}
        client.send(str(MESSAGE))
        self.server.say(f"§e[{NAME}] §aWebsocket连接成功")


    def on_message(self, client, message):
        try:
            message = dict(eval(message))
            # self.logger.info(f"[Server/{message['client']}][{message['action']}] {message['value']}")
            match message["action"]:
                case "Message":
                    self.server.say(f"§7[%s] %s"%(message["client"], message["value"]))
                case "Connection":
                    if "Connected"  in message["value"]:
                        self.server.say(f"§e[{NAME}] §a%s"%message["value"])
                    else:
                        self.server.say(f"§e[{NAME}] §cWebsocket断开连接: %s"%message["value"])
                case "Execute":
                    self.server.execute(message["value"])
                case "Request":
                    request = message["value"]
                    if request["action"] == "execute":
                        try:
                            self.request_api[request["id"]] = request["keyword"]
                            self.server.logger.info("received request")
                            f = lambda : ( time.sleep(0.1),self.server.execute(request["value"]) )
                            t = threading.Thread(target=f)
                            t.start()
                        except Exception as e:
                            self.send_return("Wrong Request: %s"%e)
                    else:
                        ...
        except Exception as e:
            self.logger.info(f"[WARN] Wrong MESSAGE format: {message} / {e}")


    def on_close(self, client, close_status_code, close_msg):
        if self.is_running:
            self.logger.info("Disconnected")
            time.sleep(10)
            self.server.logger.info("Reconnecting...")
            self.start()

    def on_info(self, info):
        if not info.is_user:
            info = info.content
            for keyword,id in zip([self.request_api[i] for i in self.request_api], list(self.request_api.keys())):
                if re.match(keyword, info):
                    self.send_return(id, info)
                    self.request_api.pop(id)
                

    def send_message(self, message: str):
        self.ws.send(str({"client": self.client_name, "action": "Message", "value": message}))
    
    def send_command(self, player, content):
        self.ws.send(str({"client": self.client_name, "action": "Command", "value": {"player": player, "content": content}}))
    
    def send_return(self, id, value):
        self.ws.send(str({"client": self.client_name, "action": "Return", "value":{"id":id, "value":value}}))

    @new_thread("lazyalienws_client")
    def start(self):

        if self.debug:
            websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open = self.on_open,
            on_message = self.on_message,
            on_close = self.on_close
        )
        self.ws.run_forever()
    
    def end(self):
        try:
            self.is_running = False
            MESSAGE = str({"client": self.client_name, "action": "Connection", "value": "Client Closed"})
            self.ws.send(MESSAGE)
            self.server.say(f"§e[{NAME}] §cWebsocket断开连接: Client closed")
            self.ws.close()
        except Exception as e:
            self.logger.info(e)

