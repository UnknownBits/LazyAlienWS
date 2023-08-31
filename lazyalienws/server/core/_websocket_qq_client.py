from websocket import WebSocketApp, ABNF
from lazyalienws.server.lib.cqhttp import API
from lazyalienws.server.logger import Logger
from lazyalienws.server.lib.help_message import HelpMessageQQ
import time, json
import threading

class QQWebSocketClient(WebSocketApp, API):

    def __init__(self, url: str, server, qq_groups: list, admin: list=[]):
        super().__init__(url, on_open=self.on_open, on_close=self.on_close, on_message=self.on_message)
        self.url = url
        self.server = server
        self.qq_groups = qq_groups
        self.uin = 1710776923 # bot的qq号
        self.logger = Logger('QQclient')
        self.help_message = HelpMessageQQ()
        self.plugins = server.plugins
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
            
            message = json.loads(message)

            try:
                if message["post_type"] != "meta_event":
                    self.logger.debug(message, module_name="Message")
            except:
                pass

            self.on_api_message(message)

            if "post_type" in message.keys() and message["post_type"] == "message":
                self.plugins.on_qq_message(self, self.server, message)
        
        except Exception as e:
            self.logger.warn(message, warn=e, module_name="Message")
    
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