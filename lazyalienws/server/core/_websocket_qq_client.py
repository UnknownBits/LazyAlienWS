from websocket import WebSocketApp, ABNF
from lazyalienws.server.lib.cqhttp import API
from lazyalienws.server.core._websocket_server import LASWebsocketServer
from lazyalienws.server.logger import Logger
import time
import threading

class QQWebSocketClient(WebSocketApp, API):

    def __init__(self, url: str, server: LASWebsocketServer, qq_groups: list, admin: list=[]):
        super().__init__(url, on_open=self.on_open, on_close=self.on_close, on_message=self.on_message)
        self.url = url
        self.server = server
        self.qq_groups = qq_groups
        self.logger = Logger('QQclient')
        self.plugins = server.plugins
        self.logger.info(", ".join(self.plugins.mixin_dictionary), module_name="Plugins")
        self.logger.info(", ".join(self.plugins.list()), module_name="Plugins")
        self.cqhttp_api = classmethod(None)
        self.admin = admin
    
    def on_open(self, client):
        self.logger.info("Connected", module_name="Connection")
        self.send_group_msg("[Server] Server Connected.")
    
    def on_close(self, client, close_status_code, close_msg):
        self.logger.info("Disconnected", module_name="Connection")
        time.sleep(10)
        self.run_forever()

    def on_message(self, client, message):

        # id = int(time.time()%10e3*10e5)
        try:
            replace_string = {"null":"None","true":"True","false":"False"}
            for i in replace_string:
                message = message.replace(i, replace_string[i])
            message = dict(eval(message))
            
            try:
                if message["post_type"] != "meta_event":
                    self.logger.debug(message, module_name="Message")
            except:
                pass

            self.on_api_message(message)

            if "post_type" in message.keys() and message["post_type"] == "message":
                self.plugins.on_qq_message(self, self.server, message)
        
        except Exception as e:
            self.logger.warn(warn=message, module_name="Message")
            self.logger.warn(warn=e, module_name="Message")
    
    def send_message(self, message):
        self.server.send_message_to_all_except("QQ",("QQ","Message",message))
    
    def send_execute(self, message):
        self.server.send_message_to_all_except("QQ",("QQ","Execute",message))
    
    def run_forever(self):
        try:
            t = threading.Thread(target=super().run_forever)
            t.daemon = True
            t.start()
        except Exception as e:
            self.logger.warn(warn=e,module_name="run-forever")
            self.close()
    

    def start(self):
        self.run_forever()
        self.logger.info("Started.")