# 控制台输入
def on_console(server, message):
    logger = server.logger.user
    get_client = server.get_client
    if " " in message:
        command = message.split(" ")

        # Send message to all client. > say <message>
        if command[0] == "say":
            try:
                msg = message[4:]
                server.send_message_to_all(("Server","Message",msg))
                logger("Send message to all: %s"%msg)
            except Exception as e:
                logger("Failed to send message to all: %s"%e)
        
        # Send message to a client. > tell <client-id or client-name> <message>
        elif command[0] == "tell":
            if len(command) == 3:
                client = get_client(command[1])
                if client == None:
                    logger("No such client")
                else:
                    try:
                        msg = message[6+len(command[1]):]
                        server.send_message(client, ("Server","action",msg))
                        if client == "QQ":
                            logger("Send message to Client-QQ/cqhttp: %s"%(msg))
                        else:
                            logger("Send message to Client-%s/%s: %s"%(client["id"],client["name"],msg))
                    except Exception as e:
                        if client == "QQ":
                            logger("Failed to send message to Client-QQ/cqhttp: %s"%(e))
                        else:
                            logger("Failed to send message to Client-%s/%s: %s"%(client["id"], client["name"], e))
            else:
                logger("Wrong arguments. > tell <client-id or client-name> <message>")
        
        # Kick a client. > kick <client-id or client-name>
        elif command[0] == "kick":
            if len(command) == 2:
                client = get_client(command[1])
                if client == None:
                    logger("No such client")
                else:
                    try:
                        server.send_message_to_all(("Server","Connection","Kicked"))
                        client['handler'].send_close()
                        logger("Kicked Client-%s/%s"%(client["id"], client["name"]))
                    except Exception as e:
                        logger("Failed to kick Client-%s/%s: %s"%(client["id"], client["name"], e))
            else:
                logger("Wrong arguments. > kick <client-id or client-name>")
        
        # Get client info. > client <client-id or client-name>
        elif command[0] == "client":
            if len(command) == 2:
                client = get_client(command[1])
                if client == None:
                    logger("None")
                else:
                    try:
                        logger("\n".join([f"  {i} : {client[i]}" for i in client]))
                    except Exception as e:
                        logger("Failed to get client info: %s"%e)
            else:
                logger("Wrong arguments. > client <client-id or client-name>")
        
        elif command[0] == "debug":
            try:
                if command[1] == "True":
                    if "DEBUG" not in server.logger.loglevel:
                        server.logger.loglevel.append("DEBUG")
                        logger("Set Server debug to True")
                    else:
                        logger("Server debug has been set to True")
                    if server.QQclient != None:
                        if "DEBUG" not in server.QQclient.logger.loglevel:
                            server.QQclient.logger.loglevel.append("DEBUG")
                            logger("Set QQ debug to True")
                        else:
                            logger("QQ debug has been set to True")
                elif command[1] == "False":
                    if "DEBUG" in server.logger.loglevel:
                        server.logger.loglevel.remove("DEBUG")
                        logger("Set Server debug to False")
                    else:
                        logger("Server debug has been set to False")
                    if server.QQclient != None:
                        if "DEBUG" in server.QQclient.logger.loglevel:
                            server.QQclient.logger.loglevel.remove("DEBUG")
                            logger("Set QQ debug to False")
                        else:
                            logger("QQ debug has been set to False")
            except:
                logger("Failed to set logger-check")
                        
    # Stop websocket-server. > stop
    
    elif message == "debug":
        logger("debug (if logger.check is used) : ")

    elif message == "help":
        logger("  help | stop | say | tell | kick | client | clients | debug")
    
    elif message == "clients":
        logger(", ".join(["QQ/cq-http"]+["client-%s/%s"%(i["id"],i["name"]) for i in server.clients]))

    else:
        try:
            logger(eval(message))
        except Exception as e:
            logger(f"Unknown command / {e}")