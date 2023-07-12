from plugins import qq_message_processing as QQmsgprocessing
from lazyalienws.api.decorator import new_thread
import json

CUSTOM = {
    "Survival": {
        "color": "e",
        "zh_cn": "生存"
    },
    "Creative": {
        "color": "a",
        "zh_cn": "创造"
    },
    "Mirror": {
        "color": "6",
        "zh_cn": "镜像"
    },
    "Void": {
        "color": "3",
        "zh_cn": "虚空"
    },
    "Velocity": None
}

latest_game_info = {"player":None, "action":None, "client":None}

def on_message(client, server, message):
    custom = CUSTOM[client["name"]]
    if custom:
        if message.value[-2:] == "游戏": return
        msg = "§8[§%s%s§8]§f %s"%(custom["color"],custom["zh_cn"],message.value)
        server.logger.info(msg, module_name="Message")
        msg = 'tellraw @a {"text":"%s"}'%msg
        server.send_message_to_all_except(["QQ",client], (client["name"],"Execute",msg))
        server.send_message("QQ", (custom["zh_cn"],"Message",QQmsgprocessing.fix_cq(message.value)))
    else:
        server.QQclient.send_group_msg(message.value)

@new_thread
def on_qq_message(QQclient, server, message): # 处理qq信息 主要处理cq码并转发mc
    try:
        keys = list(message.keys())
        if "post_type" in keys: # 参见 cqhttp-api 文档
            if message["post_type"] == "message": # 类型为消息

                if message["message_type"] == "group" and message["group_id"] in QQclient.qq_groups: # 群消息
                    message_content = message["message"] # 发送的消息
                    # message_content = QQmsgprocessing.qq_message_processing(QQclient, message)
                    if message_content != None:
                        # execute_value = QQmsgprocessing.fix_braces(message_content[9:])
                        execute_value = QQmsgprocessing.CQprocessing(QQclient,message)()
                        QQclient.send_execute(execute_value)
                        info = "".join([i["text"] for i in json.loads(execute_value[11:])])
                        QQclient.logger.info(info, module_name="Message")
                        return 
                    else:
                        return 
            else:
                message = None
    except Exception as e:
        if "replace() argument 2 must be str, not None" in str(e) or "'NoneType' object is not subscriptable" in str(e):
            return 
        raise e