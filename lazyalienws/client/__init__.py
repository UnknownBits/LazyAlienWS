from mcdreforged.api.decorator import new_thread
from mcdreforged.api.types import ServerInterface
import websocket
import time, threading

class MCDR_velocity_plugin:

    def __init__(self, server:ServerInterface, url:str, client_name:str) -> None:
        if client_name == None:
            server.logger.info("Change the client name in config.")
            server.say(r"§e[LAS-plugin-WebsocketVer.] §c终止§f: §4必须在配置文件中设置客户端名称")
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
            server.say(r"§e[LAS-plugin-WebsocketVer.] §c终止§f: §4必须在配置文件中设置客户端名称")
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
        self.ws.on_info(info)
    
    def on_player_joined(self, server, player, info):
        ip = info.content.replace(player,'').split(' logged in with')[0]
        server.logger.info(f'player:{player}, ip:{ip}, action:logged')
        if ip == "[local]":
            self.ws.send_message("[BOT]%s 加入了游戏"%player)
            server.execute("execute as %s run team join bot"%player)
        else:
            # self.ws.send_message("%s 加入了游戏"%player)
            self.ws.send_command(player, "#LAS")
        
        if player[0] in "Bb" and player[1] in "Oo" and player[2] in "Tt" and player[3] == "_" and ip != "[local]":
            server.execute("kick %s DO NOT user nickname with the '%s' prefix"%(player,player[:4]))
    
    def on_player_left(self, server, player):
        # self.ws.send_message("%s 退出了游戏"%player)
        pass
    
    def on_unload(self, server):
        self.ws.end()
    
    def on_server_startup(self, server):
        server.execute("team add bot")
        server.execute('team modify bot prefix {"text":"[BOT]","color":"aqua"}')
        server.execute('team modify bot displayName {"text":"bot"}')
        self.ws.send_message('Server Started')

    def on_server_stop(self, server, server_return_code):
        self.ws.send_message('Server Stoped: %s'%server_return_code)


class MCDR_WebSocketClient:

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
        self.server.say("§e[LAS-plugin-WebsocketVer.] §aWebsocket连接成功")


    def on_message(self, client, message):
        # self.logger.info(f"{message}")
        try:
            message = dict(eval(message))
            # self.logger.info(f"[Server/{message['client']}][{message['action']}] {message['value']}")
            if message["action"] == "Message":
                self.server.say(f"§7[%s] %s"%(message["client"], message["value"]))
            elif message["action"] == "Connection":
                if "Connected"  in message["value"]:
                    self.server.say("§e[LAS-plugin-WebsocketVer.] §a%s"%message["value"])
                else:
                    self.server.say("§e[LAS-plugin-WebsocketVer.] §cWebsocket断开连接: %s"%message["value"])
            elif message["action"] == "Execute":
                self.server.execute(message["value"])
            elif message["action"] == "Request":
                request = message["value"]
                if request["action"] == "execute":
                    try:
                        self.request_api[request["id"]] = request["keyword"]
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
            time.sleep(5)
            self.server.logger.info("Reconnecting...")
            self.start()

    def on_info(self, info):
        if not info.is_user:
            info = info.content
            for keyword,id in zip([self.request_api[i] for i in self.request_api], list(self.request_api.keys())):
                if keyword in info:
                    if keyword in info:
                        self.send_return(id, info)
                        self.request_api.pop(id)
                

    def send_message(self, message: str):
        self.ws.send(str({"client": self.client_name, "action": "Message", "value": message}))
    
    def send_command(self, player, content):
        self.ws.send(str({"client": self.client_name, "action": "Command", "value": {"player": player, "content": content}}))
    
    def send_return(self, id, value):
        self.ws.send(str({"client": self.client_name, "action": "Return", "value":{"id":id, "value":value}}))

    @new_thread("LAS WebSocketClient")
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
            self.server.say("§e[LAS-plugin-WebsocketVer.] §cWebsocket断开连接: Client closed")
            self.ws.close()
        except Exception as e:
            self.logger.info(e)

