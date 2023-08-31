def webs(content):
    if content == "#官网":
        return "https://lazyalienserver.top"
    elif content == "#赞助":
        return "https://afdian.net/a/tanh_Heng"
    elif content == "#bluemap":
        return "没写"
    elif content == "#status":
        return "没写"

def on_qq_message(QQclient, server, message):
    content = message["message"]
    web = webs(content)
    if web != None:
        msg = "%s %s"%(content[1:],web)
        QQclient.send_msg(msg, message)

def on_command(client, server, player, command):
    web = webs(command)
    if web != None:
        web = 'tellraw %s [{"text":"§e[%s] "},{"text":"§b§n%s","clickEvent":{"action":"open_url","value":"%s"},"hoverEvent":{"action":"show_text","value":{"text":"§b在网页打开"}}}]'%(player,command[1:],web,web)
        server.send_message(client,("Server","Execute",web))