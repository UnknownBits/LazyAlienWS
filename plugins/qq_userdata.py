from lazyalienws.api.data import Data
from lazyalienws.server.lib.exception import raise_exception

class User:

    def __init__(self, filepath="LAS-websocket-server/data/user_data.json") -> None:
        self.file = Data("user_data.json")
        self.users = self.file.load()
    
    def _is_sender_has_binded(self, sender):
        return bool([i for i in self.users if i["qq_id"] == sender])

    def _get_sender_index(self,sender):
        return [i["qq_id"] for i in self.users].index(sender)

    def bind(self,sender,Mcid) -> bool :
        if not self._is_sender_has_binded(sender):
            self.users.append({"qq_id":sender,"mc_id":"","nickname":""})
        ind = self._get_sender_index(sender)
        if self.users[ind]["mc_id"]=="":
            self.users[ind]["mc_id"]=Mcid
            self.file.write(self.users)
            return True
        else:
            return False
    
    def unbind(self,sender) -> bool :
        flag=False
        for i in self.users:
            if i["qq_id"]==sender:
                flag=True
        if flag==True:
            ind = self._get_sender_index(sender)
            if self.users[ind]["mc_id"]=="":
                return False
            else:
                self.users[ind]["mc_id"]=""
                self.file.write(self.users)
                return True
        else:
            return False
        
    def change_nickname(self,sender,new_nickname) -> bool:
        if self._is_sender_has_binded(sender):
            ind=self._get_sender_index(sender)
            self.users[ind]["nickname"]=new_nickname
            self.file.write(self.users)
            return True
        else:
            return False
       
user=User()

def on_qq_message(QQclient, server, message: dict):
    
    message_content = message["message"]
    sender = message["sender"]["user_id"]
    
    if message_content[:7]=="#绑定mcid" and len(message_content)>8:
        Mcid=message_content[8:]
        if user.bind(sender,Mcid):
            try:
                user.bind(sender,Mcid)
                QQclient.logger.info("Binded mcid",module_name="userdata")
                msg=f"[CQ:at,qq={sender}]绑定成功"
                QQclient.send_msg(msg,message)
            except Exception as e:
                QQclient.logger.warn("Failed to bind mcid",warn=e,module_name="userdata")
                raise_exception(e)
                msg=f"[CQ:at,qq={sender}]绑定失败"
                QQclient.send_msg(msg,message)
        else:
            msg=f"[CQ:at,qq={sender}]绑定失败:已绑定游戏角色"
            QQclient.send_msg(msg,message)
    
    if message_content[:5]=="#取消绑定":
        try:
            user.unbind(sender)
            QQclient.logger.info("Unbinded mcid",module_name="userdata")
            msg=f"[CQ:at,qq={sender}]解绑成功"
            QQclient.send_msg(msg,message)
        except Exception as e:
            QQclient.logger.warn("Failed to bind mcid",warn=e,module_name="userdata")
            raise_exception(e)
            msg=f"[CQ:at,qq={sender}]解绑失败:问题已抛出,请联系管理员获得解决"
            QQclient.send_msg(msg,message)
            
    if message_content[:5]=="#修改昵称" and len(message_content)>6:
        new_nickname=message_content[6:]
        try:
            if user.change_nickname(sender=sender,new_nickname=new_nickname):
                QQclient.logger.info("Changed nick name",module_name="userdata")
                msg=f"[CQ:at,qq={sender}]修改成功"
                QQclient.send_msg(msg,message)
            else:
                QQclient.logger.info("Failed to change nick name",module_name="userdata")
                msg=f"[CQ:at,qq={sender}]请先绑定mcid!"
                QQclient.send_msg(msg,message)
        except Exception as e:
            QQclient.logger.warn("Failed to change nick name",warn=e,module_name="userdata")
            raise_exception(e)
            msg="解绑失败:问题已抛出,请联系管理员获得解决"
            QQclient.send_msg(msg,message)
        
    else:
        return
    
    
    server.logger.info("text",module_name="123")

   