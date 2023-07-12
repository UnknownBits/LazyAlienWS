def on_qq_message(QQclient, server, message: dict):
    
    message_content = message["message"]
    sender = message["sender"]

    if message_content[:5] == "#合并转发":
        if len(message_content) >7 and message_content[6] == "$":
            if sender["user_id"] in QQclient.admin:
                try:
                    forward_msg = message_content.split("$")[1].split(',')
                    forward_msg = {"name":forward_msg[0],"uin":int(forward_msg[1]), "content":",".join(forward_msg[2:])}
                except Exception as e:
                    QQclient.send_group_msg("参数错误: %s"%e, message["group_id"])
                    return 
            else:
                QQclient.send_group_msg("权限不足", message["group_id"])
                return 

        else:
            sender_name = sender["card"] # 发送者群昵称
            if sender_name == '':
                sender_name = sender["nickname"]
            
            if len(message_content) >5 and message_content[5] == ' ':
                forward_msg = {"name":sender_name,"uin":sender["user_id"],"content":message_content[6:]}
            else:
                QQclient.send_group_msg("#合并转发 内容\n#合并转发 $name,uin,msg", message["group_id"])
                return 
        QQclient.logger.info("#合并转发: %s"%forward_msg, module_name="qq_command")
        QQclient.send_group_forward_msg(message["group_id"], forward_msg)
    
    # elif message_content[:5] == "#在线玩家":