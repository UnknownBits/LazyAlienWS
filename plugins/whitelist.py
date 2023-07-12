import threading

def whitelist_handler(QQclient, server, message, server_name, value):
    if value.split(' ')[1] in ["on","off"]:
        keyword = "Whitelist"
    else:
        keyword = "whitelist" # 参见 源码library/
    msg = server.create_request(client=server.get_client(server_name),value=value,keyword=keyword)
    QQclient.send_msg(msg, message)

def on_qq_message(QQclient, server, message):
    content = message["message"]
    if content == "#whitelist":
        msg = '''格式 #whitelist 参数 子服名
生存服白名单 : at tanh_Heng/CatCoinZHSM/RCY_QWQ/Fanzhitianyu
创造服白名单 : 提交红石(RCY/Fanzhitianyu)/建筑(tanh_Heng/Terry)作品
虚空服 : 需测试机器时向tanh_Heng申请开启'''
        QQclient.send_msg(msg, message)
    elif content[:10] == "#whitelist":
        if message["sender"]["user_id"] in QQclient.admin:
            try:
                command = content.split(' ')
                server_name = command[-1]
                if server_name in [i["name"] for i in server.clients]:
                    value = ' '.join(command[:-1])[1:]
                    t = threading.Thread(target=whitelist_handler, args=(QQclient, server, message, server_name, value))
                    t.daemon = True
                    t.start()
                else:
                    QQclient.send_msg("未知的客户端: %s"%server_name, message)
            except:
                QQclient.send_msg("参数错误"%server_name, message)
        else:
            QQclient.send_msg("权限不足", message)

