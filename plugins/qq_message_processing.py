import re, json
from typing import Any
from lazyalienws.server.lib.exception import raise_exception
from lazyalienws.api.data import Data

def fix_cq(string): # /@ -> CQ:at,qq= ; /! -> CQ:reply,id=
    return re.sub(r"\(!(-?[0-9]+?)\)","[CQ:reply,id=\g<1>]",re.sub(r"\(@([0-9]+?)\)","[CQ:at,qq=\g<1>]",string))

class CQprocessing:

    def __init__(self, QQclient, message) -> None:
        self.QQclient = QQclient
        self.message = message
    
    def __call__(self) -> Any:
        return self.message_processing(self.message)

    def get_cq_info(self, string): # 匹配cq码，提取为字典
        cq_type = re.match(r"\[CQ:([^,\]]+)[^\]]+]",string)
        if cq_type:
            return {i[0]:i[1] for i in [("CQ",cq_type.groups()[0])]+re.findall(r",([^=]+)=([^,\]]+)", string)}
    
    def split_text(self, string): # 切分cq与普通字符串
        content_list = re.split(r"(\[CQ:[^\]]+?])",string)
        while '' in content_list:
            content_list.remove('')
        return content_list
    
    def is_cq(self, string): # 判断某字符串是否为cq码
        return re.fullmatch(r'\[CQ:[^\]]+?]',string) != None
    
    def to_jsondict(self, string, is_reply_msg=False): # 将cq/文本转为jsondict
        if self.is_cq(string):
            QQclient = self.QQclient
            cq_info = self.get_cq_info(string)
            match cq_info["CQ"]:
                case "image":
                    if "subType" in cq_info.keys():
                        match cq_info["subType"]:
                            case "0":
                                image_type = "[图片]"
                            case "1":
                                image_type = "[表情]"
                            case _:
                                image_type = "[图片]"
                                raise_exception(RuntimeError(f"Unknown subType: {cq_info['subType']}"))
                    else:
                        image_type="[图片]"
                        QQclient.logger.info("image info had no key 'subType': {}".format(cq_info))
                    msg = [{"text":"§2§n%s§r"%image_type,
                            "clickEvent":{"action":"open_url","value":cq_info["url"]},
                            "hoverEvent":{"action":"show_text","value":{"text":"§a%s\n§7§o单击以在网页查看"%image_type}}}]
                case "reply":
                    reply_msg_value = QQclient.get_msg(cq_info["id"])
                    if reply_msg_value["data"]:
                        reply_message = self.message_processing(reply_msg_value["data"], is_reply_msg=True) # 处理回复的消息
                        msg = [{"text":"「回复 “"}]+reply_message+[{"text":"”」"}]
                    else:
                        msg = {"text":'「回复 §7...§r 」'}
                case "at":
                    qq = cq_info["qq"]
                    if qq == "all":
                        msg = {"text":"§e@全体成员§f"}
                    else:
                        group_member_info = QQclient.get_group_member_info(self.message["group_id"], qq)["data"]
                        if group_member_info["card"] == '':
                            at_qq = group_member_info["nickname"]
                        else:
                            at_qq = group_member_info["card"]
                        msg = {"text":"@"+at_qq}
                case "forward":
                    msg = {"text":"[合并转发]"}
                case _:
                    raise_exception(RuntimeError("CQ cannot be processed: %s"%string))
                    msg = {"text":"[?]"}
        else:
            msg = {"text":string}
        if is_reply_msg:
            if type(msg) == dict:
                msg["color"] = "gray"
                msg["italic"] = True
            elif type(msg) == list:
                for i in msg:
                    i["color"] = "gray"
                    i["italic"] = True
        if type(msg) != list:
            msg = [msg]
        return msg
    
    def message_processing(self, message, is_reply_msg=False):
        message_content = message["message"]
        QQclient = self.QQclient
        
        sender = message["sender"] # 获取sender
        if "user_id" in sender.keys() and sender["user_id"] == QQclient.uin and is_reply_msg:
            sender_name = None
        else:
            # users=Data("user_data.json").load()
            # ind=[i["qq_id"] for i in users].index(sender)
            # if not users[ind]["nickname"]=="":
            #     sender = {"card":users[ind]["nickname"]}
            #     sender = {"card":"The nickname you want to replace"}
            if False:
                ...
            elif "card" in sender.keys():
                ...
            elif "user_id" in sender.keys():
                sender = QQclient.get_group_member_info(message["group_id"],sender["user_id"])["data"]
            else:
                sender = {"card":"UNKNOWN"}
                QQclient.logger.warn(warn=AttributeError("Message with unknown sender: %s"%message))
            sender_name = sender["card"] # 发送者群昵称
            if sender_name == '':
                sender_name = sender["nickname"]
        
        content_list = [i for k in [self.to_jsondict(i,is_reply_msg=is_reply_msg) for i in self.split_text(message_content)] for i in k] # 处理cq
        if is_reply_msg: # 上面的多层generator是用来将嵌套列表展开的
            if sender_name:
                return [{"text":"§7§o<%s>§r "%sender_name}] + content_list
            else:
                return content_list
        else:
            QQ_clickReply = {"text":"§8[§d QQ §8]§r","insertion":"(!%s)"%(message["message_id"]),"hoverEvent":{"action":"show_text","value":{"text":"§d回复该消息\n§7§oSHIFT+左键"}}}
            user_clickAt = {"text":"§f<§7%s§f>§r"%sender_name,"insertion":"(@%s)"%(sender["user_id"]),"hoverEvent":{"action":"show_text","value":{"text":"§b@%s\n§7§oSHIFT+左键"%sender_name}}}
            content_list = [{"text":""},QQ_clickReply,{"text":" "},user_clickAt,{"text":" "}] + content_list
            return "tellraw @a %s"%(json.dumps(content_list).replace("&#91;","[").replace("&#93;","]"))

# 为什么要看我以前写的答辩呜呜呜呜呜呜呜
# def fix_braces(string): # 修复中括号
#     return string.replace("&#91;","[").replace("&#93;","]")

# def qq_message_processing(QQclient, message: dict, is_reply_msg = False):
#     '''qq message processing'''
#     # qq cq处理
#     QQclient.logger.debug('===== START =====', module_name = "CQ-processing/Main")
#     QQclient.logger.debug('message_content: %s'%message, module_name = "CQ-processing/Main")
    
#     # 设置message_content
#     message_content = message["message"] 
    
#     # 获取sender_name发送者昵称
#     sender = message["sender"]
#     if "user_id" in sender.keys() and sender["user_id"] == QQclient.uin and is_reply_msg:
#         sender_name = None
#     else:
#         if "card" in sender.keys():
#             ...
#         elif "user_id" in sender.keys():
#             sender = QQclient.get_group_member_info(message["group_id"],sender["user_id"])["data"]
#         else:
#             sender = {"card":"UNKNOWN"}
#             QQclient.logger.warn(warn=AttributeError("Message with unknown sender: %s"%message))
#         sender_name = sender["card"] # 发送者群昵称
#         if sender_name == '':
#             sender_name = sender["nickname"]

#         # 获取多CQ码文本列表
#     cq_content_list = [("[CQ:"+i.split("]")[0])+"]" for i in message_content.split("[CQ:")[1:]]

#     # 多CQ码文本列表转多CQ码字典列表
#     cq_list = []
#     for cq_content in cq_content_list:
#         cq_values_dict = {}
#         for cq_value in [{k.split("=")[0]:"=".join(k.split("=")[1:])} for k in cq_content.replace('[CQ:','CQ=')[:-1].split(',')]:
#             cq_values_dict.update(cq_value)
#         cq_list.append(cq_values_dict)
#     QQclient.logger.debug('cq_list: 「%s」 -> 「%s」'%(cq_content_list, cq_list), module_name = "CQ-processing/Main")

#     # 将CQ码文本替换为CQ码对应元素
#     for cq_content, cq_value in zip(cq_content_list, cq_list):
#         cq_content_replace = cq_dict_processing(QQclient, cq_value, message, is_reply_msg)
#         if cq_value["CQ"] == "reply": # 如果为CQ-reply 去掉reply后多出的at
#             cq_replyat_index = cq_content_list.index(cq_content)+1
#             cq_content = cq_content+cq_content_list[cq_replyat_index]
#         message_content = message_content.replace(cq_content, cq_content_replace)
#         QQclient.logger.debug('cq_content->cq_value replace: 「%s」 -> 「%s」'%(cq_content, cq_content_replace), module_name = "CQ-processing/Main")
    
#     if "[!]" in message_content: # 含[!]将全部消息替换为[!]中间的内容
#         message_content = message_content.split("[!]")[1]

#     json_list = []
#     for content in message_content.split('[SPLIT]'):
#         if content[:6] == "[json]":
#             json_list.append(content[6:])
#         else:
#             if is_reply_msg:
#                 custom = "§7§o"
#             else:
#                 custom = "§f"
#             json_list.append('{"text":"%s%s§r"}'%(custom,content.replace('"',r'\"')))
    
#     if is_reply_msg:
#         if sender_name:
#             message_content = "[SPLIT][json]%s[SPLIT]"%",".join(['{"text":"§7§o<%s>§r "}'%sender_name] + json_list)
#         else:
#             message_content = "[SPLIT][json]%s[SPLIT]"%",".join(json_list)
#     else:
#         message_id = message["message_id"]
#         user_id = sender["user_id"]
#         space = '{"text":" "}'
#         QQ_clickReply = '{"text":"§8[§d QQ §8]§r","insertion":"(!%s)","hoverEvent":{"action":"show_text","value":{"text":"§d回复该消息\\n§7§oSHIFT+左键"}}}'%(message_id)
#         user_clickAt = '{"text":"§f<§7%s§f>§r","insertion":"(@%s)","hoverEvent":{"action":"show_text","value":{"text":"§b@%s\\n§7§oSHIFT+左键"}}}'%(sender_name,user_id,sender_name)
#         message_content = "[execute]tellraw @a [%s]"%",".join(['{"text":""}',QQ_clickReply, space, user_clickAt, space] + json_list)

#         message_content = message_content.replace("\r","").replace("\n","") # 去掉转义符

#         QQclient.logger.debug('message_content: %s'%message_content, module_name = "CQ-processing/Main")
#         QQclient.logger.debug('===== END =====', module_name = "CQ-processing/Main")
    
#     return message_content


# # 处理cq_dict
# def cq_dict_processing(QQclient, cq_dict: dict, message: dict=None, is_reply_msg=False):
#     '''cq dict -> str'''

#     if cq_dict == None:
#         return 
    
#     if cq_dict["CQ"] == "image": # CQ-image
#         subType = cq_dict["subType"]
#         if subType == "0":
#             image_type = "[图片]"
#         elif subType == "1":
#             image_type = "[表情]"
#         else:
#             image_type = "[图片]"
#             QQclient.logger.debug(f"Unknown subType: {subType}", module_name = "CQ-processing/image")
#         message = ('''[SPLIT][json]{"text":"%s","underlined":true,"color":"dark_green","clickEvent":{"action":"open_url","value":"%s"},"hoverEvent":{"action":"show_text","value":{"text":"§a%s\\n§7§o单击以在网页查看"}}}[SPLIT]'''%(image_type, cq_dict["url"], image_type))
    
#     elif cq_dict["CQ"] == "at": # CQ-at
#         qq = cq_dict["qq"]
#         if qq == "all":
#             message = "§e@全体成员§f"
#         else:
#             group_member_info = QQclient.get_group_member_info(message["group_id"], qq)["data"]
#             if group_member_info["card"] == '':
#                 at_qq = group_member_info["nickname"]
#             else:
#                 at_qq = group_member_info["card"]
#             message = "@"+at_qq

#     elif cq_dict["CQ"] == "reply": # CQ-reply
#         reply_msg_value = QQclient.get_msg(cq_dict["id"])
#         if reply_msg_value["data"]:
#             reply_message = qq_message_processing(QQclient, reply_msg_value["data"], is_reply_msg=True) # 处理回复的消息
#             message = f'「回复 “{reply_message}”」'
#         else:
#             message = f'「回复 §7...§r 」'
#         QQclient.logger.debug("CQ reply: %s"%message)
#     elif cq_dict["CQ"] == "forward":
#         message = "[!][合并转发][!]"
#     else: # 未处理的CQ
#         QQclient.logger.warn(warn=AttributeError("CQ cannot be processed: %s"%str(message)), module_name = "CQ-processing/UNKNOWN")
#         message = "[CQ]"
    
#     return message