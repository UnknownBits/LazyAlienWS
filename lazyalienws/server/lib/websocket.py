import time, random
from websocket_server import WebsocketServer

class API(WebsocketServer):
    
    # Message字符串格式化classmethod
    def message(self, message: str) -> classmethod | None:
        '''message str -> classmethod'''
        try:
            message = dict(eval(message))
            msg = classmethod(None)
            msg.client = message["client"]
            msg.action = message["action"]
            msg.value = message["value"]
            return msg
        except Exception as e:
            self.logger.warn(f"Wrong MESSAGE format: {message}", warn=e, module_name="Message")
            return 
    

    # 消息发送
    def create_message(self, msg: tuple):
        '''message tuple -> str(dict)'''
        if (type(msg) == tuple) and sum([1 for i in msg if type(i) == str]) == 3:
            return str({"client":msg[0], "action":msg[1], "value":msg[2]})
        else:
            return msg
    def send_message(self, client, msg: object|tuple):
        'msg: object|tuple / msg tuple:(client,action,value)'
        if client == "QQ" and self.QQclient:
            self.QQclient.send_group_msg(f"[{msg[0]}] {msg[2]}")
        else:
            super().send_message(client, self.create_message(msg))
    def send_message_to_all(self, msg):
        'msg: object|tuple / msg tuple:(client,action,value)'
        super().send_message_to_all(self.create_message(msg))
        if self.QQclient:
            self.QQclient.send_group_msg(f"[{msg[0]}] {msg[2]}")
    def send_message_to_all_except(self, client, msg):
        'msg: object|tuple / msg tuple:(client,action,value)'
        if client == "QQ":
            super().send_message_to_all(self.create_message(msg))
        else:
            if self.QQclient:
                self.QQclient.send_group_msg(f"[{msg[0]}] {msg[2]}")
            for i in self.clients:
                if i != client:
                    self.send_message(i, msg)
    
    # 请求发送
    def create_request(self, client, action:str="execute", value=None, keyword=None, timeout=10):
        t = time.time()
        id = int(sum(bytes(client["name"], encoding="utf-8"))*10e10+t*10e8%10e10)      
        self.logger.debug(f"id: {id}({t})", module_name="Request")
        timeout = int(timeout)
        if action == "execute":
            if value and keyword:
                request = {"id":id, "action":action, "value":value, "keyword":keyword} 
            else:
                return AttributeError("execute")
        elif action == 'eval':
            if value:
                request = {"id":id, "action":action, "value":value}
            else:
                return AttributeError("eval")
        
        self.logger.debug(f"id/{id} request -> {client['name']}: {request}", module_name="Request")
        
        super().send_message(client, str({"client":"Server", "action":"Request", "value":request}))
        self.request_api[id] = None
        
        for i in range(timeout*10):
            if self.request_api[id]:
                break
            time.sleep(0.1)
            
        if i == timeout*10-1:
            self.logger.debug(f"id/{id} {client['name']} Timeout", module_name="Request")
            return None
        else:
            self.logger.debug(f"id/{id} {client['name']} -> value: {self.request_api[id]}", module_name="Request")
            return self.request_api[id]
        
    def on_request_message(self, message):
        try:
            self.request_api[message.value["id"]] = message.value["value"]
        except Exception as e:
            self.logger.warn("Wrong Return format: %s"%message.value, warn=e, module_name="Request")
    
    # 按客户端名称或id获取客户端信息
    def get_client(self, client_id_or_name: str | int):
        '''Get client info by client-id or client-name'''
        if client_id_or_name == "QQ":
            return "QQ"
        try:
            client_id = eval(client_id_or_name)
            if type(client_id) == int:
                return self.clients[[i["id"] for i in self.clients].index(client_id)]
        except:
            if type(client_id_or_name) == str:
                client_name = client_id_or_name
                client_names = [i["name"] for i in self.clients]
                if client_name in client_names:
                    return self.clients[client_names.index(client_name)]
                else:
                    return None
