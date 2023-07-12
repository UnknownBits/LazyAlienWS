import threading, time

tick_health = {}
all_client_names = ["Survival","Creative","Void","Mirror"]
on_tps = False

def on_qq_message(QQclient, server, message):
    t = threading.Thread(target=on_qq_message_handler, args=(QQclient, server, message))
    t.daemon = True
    t.start()

def on_qq_message_handler(QQclient, server, message):
    global tick_health, on_tps
    
    message_content = message["message"]
    if message_content[:5] in ["#tps","#mspt"]:
        command = message_content.split(" ")
        
        if len(command) == 1:
            if on_tps:
                QQclient.send_msg("当前已有tps与mspt请求",message)
            else:
                on_tps = True
                try:
                    QQclient.send_msg("正在请求tps与mspt...",message)
                    client_names = get_tick_health(server, server.clients)
                    info = "\n".join(["[%s]\n * tps %s / mspt %s"%(n,h["tps"],h["mspt"]) for n,h in zip(client_names, [tick_health[client_name] for client_name in client_names])])
                    disconnected_clients = list(set(all_client_names)-set([i["name"] for i in server.clients]))
                    if disconnected_clients != []:
                        info = "\n".join([info,"\n".join(["[%s]\n * 未连接"%client_name for client_name in disconnected_clients])])
                    QQclient.send_msg(info,message)
                except:
                    pass
                on_tps = False

def get_tick_health(server, client: dict|list, timeout=10):
    global tick_health
    
    if type(client) == list:
        clients = [i for i in client if i["name"] in all_client_names]
        for client in clients:
            tick_health[client["name"]] = None
            server.logger.debug("get-tick-health: %s"%client, module_name="tick-health/clients")
            t = threading.Thread(target=get_tick_health, args=(server, client, timeout))
            t.daemon = True
            t.start()
        while True:
            if None not in [tick_health[client["name"]] for client in clients]:
                break
            time.sleep(0.1)
        server.logger.debug("tick health info: %s"%[tick_health[client["name"]] for client in clients], module_name="tick-health/clients")
        return [i for i in tick_health if tick_health[i] != None and i in all_client_names]
    elif type(client) == dict:
        tps = server.create_request(client, value="tick rate", keyword="Current tps is: ", timeout=timeout)
        if tps: mspt = server.create_request(client, value="tick health", keyword="Average tick time: ", timeout=timeout);
        else: mspt = None
        if tps: tps = tps.replace("Current tps is: ","");
        else: tps = "Unknown"
        if mspt: mspt = mspt.replace("Average tick time: ","");
        else: mspt = "Unknown"
        tick_health[client["name"]] = {"tps":tps,"mspt":mspt}
        server.logger.debug("%s : %s"%(client["name"],tick_health[client["name"]]), module_name="tick-health/client")
    else:
        server.logger.warn("Wrong client type to request: %s / %s"%(type(client), client), module_name="tick-health")