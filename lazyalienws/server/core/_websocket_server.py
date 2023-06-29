from websocket_server import WebsocketServer
import logging, threading, time
from lazyalienws.server.logger import Logger
from lazyalienws.server.plugin import Plugins
from lazyalienws.server.lib.websocket import API
from lazyalienws.server.lib.mcdr import MCDR_API


# LASWebsocketServer 继承自API&websocket_server.WebsocketServer
class LASWebsocketServer(API, MCDR_API):

    # __init__ 初始化WebsocketServer&logger
    def __init__(self, host='127.0.0.1', port=5800, loglevel=logging.WARNING, key=None, cert=None):
        super().__init__(host, port, loglevel, key, cert)
        self.QQclient = None
        self.request_api = {}
        self.logger = Logger("WSserver")
        self.plugins = Plugins() # 加载plugin
        self.logger.info(", ".join(self.plugins.mixin_dictionary), module_name="Plugins")
        self.logger.info(", ".join(self.plugins.list()), module_name="Plugins")


    # 新的client连接
    def new_client(self, client, server):
        super().new_client(client, server)
        client["name"] = None
        info = f"CLIENT-{client['id']} Connected"
        self.logger.info(info, module_name="Connection")
    

    # client断开
    def client_left(self, client, server):
        super().client_left(client, server)
        info = f"CLIENT-{client['id']}/{client['name']} Disconnected"
        self.logger.info(info, module_name="Connection")
    

    # 关闭client连接
    def close_client(self, client):
        client["handler"].send_close()


    # 收到消息
    def message_received(self, client, server, message):
        super().message_received(client, server, message)

        try:

            # 格式化MESSAGE
            message = self.message(message)
            if message == None:
                return 
            
            # 如果MESSAGE非请求连接 且该client未设置client-name 踢出
            if (client["name"] == None) and not ((message.action == "Connection") and (message.value == "Connected") and (message.client != None)):
                self.send_message(client, ("Server","Connection","Wrong client-name"))
                self.logger.info(f"CLIENT-{client['id']} Wrong client-name: {message.action},{message.value},{message.client}",module_name="Message")
                self.close_client(client)
                return
            
            else:
                info = f"CLIENT-{client['id']}/{message.client} {message.action} : {message.value}"
                self.logger.info(info, module_name="Message")

                # 信息类型为Connection
                if message.action == "Connection":

                    # 初次连接
                    if message.value == "Connected":
                        client["name"] = message.client

                        # 踢出重名client
                        if client["name"] in [i["name"] for i in self.clients]:
                            client_name = client["name"]
                            client_id = client["id"]
                            for i in self.clients:
                                if (i["name"] == client_name) and (i["id"] != client_id):
                                    self.send_message(i, ("Server","Connection","Wrong client-name"))
                                    self.close_client(i)
                        
                        # 广播有client连接了
                        self.send_message_to_all_except(client, ("Server","Connection","Client-%s/%s Connected"%(client["id"], client["name"])))
                    
                    return 
                
                elif message.action == "Message":
                    self.plugins.on_message(client, self, message)
                    # self.send_message_to_all_except(client, (client["name"],"Message",message.value))
                
                elif message.action == "Command":
                    try:
                        content = dict(message.value)
                        player = content["player"]
                        command = content["content"]
                        self.plugins.on_command(client, self, player, command)
                    except Exception as e:
                        self.logger.warn(warn=e,module_name="Command")
                
                elif message.action == "Return":
                    self.on_request_message(message)
        
        except Exception as e:
            self.logger.warn(warn=e, module_name="Message")
    
    def user_input(self):

        while True:

            try:
                message = input()
                if message == "stop":
                    self.send_message_to_all_except("QQ",("Server","Connection","Server Closed."))
                    for i in self.clients:
                        self.close_client(i)
                    self.send_message("QQ",("Server","Connection","Server Closed."))
                    break
                self.plugins.on_console(self, message)

            except Exception as e:
                self.logger.warn(warn=e,module_name="User")
    
    def start(self):
        t = threading.Thread(target=self.run_forever, args=())
        t.daemon = True
        t.start()

        self.plugins.on_start(self)

        time.sleep(0.1)
        self.logger.info("Started.")
        self.user_input()
        self.logger.info("Closed.")