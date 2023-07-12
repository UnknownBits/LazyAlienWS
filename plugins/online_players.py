from mcstatus import JavaServer
from lazyalienws.server.core._websocket_qq_client import QQWebSocketClient
from lazyalienws.server.lib.exception import raise_exception
from lazyalienws.api.decorator import new_thread
import time

servers = {
    "Survival": "127.0.0.1:25585",
    "Creative": "127.0.0.1:25586",
    "Mirror": "127.0.0.1:25587",
    "Void": "127.0.0.1:25588"
}

def get_online_players(servers: dict, ws_server: QQWebSocketClient):
    online_players = {}
    for server in servers.keys():
        try:
            mc_server = servers[server].split(":")
            mc_server = JavaServer(mc_server[0], int(mc_server[1]))
            players = mc_server.query().players.names
            # bot = [i for i in players if i[0] in "Bb" and i[1] in "Oo" and i[2] in "Tt" and i[3] == "_"]
            team_bot = ws_server.create_request(ws_server.get_client(server), value="team list bot", keyword="eam [bot]")
            if team_bot:
                if "no members" in team_bot:
                    bot = []
                else:
                    bot = team_bot.split("members:")[1].replace(" ","").split(",")
            else:
                bot = []
            real_players = list(set(players)-set(bot))
            online_players[server] = {"players":real_players, "bots":bot}
        except ConnectionResetError:
            online_players[server] = None
            pass
        except Exception as e:
            online_players[server] = None
            raise_exception(e)
            # QQclient.logger.warn(server,warn=e, module_name="onlien-players")
    return online_players

@new_thread
def on_qq_message(QQclient, server, message):
    if message["message"] == "#在线玩家":
        time.sleep(0.1)
        online_players = get_online_players(servers, server)
        online_players_info = []
        for s in online_players:
            if online_players[s] == None:
                online_players_info = online_players_info + [f"[{s}] 未运行"]
            else:
                players = online_players[s]["players"]
                bots = online_players[s]["bots"]
                online_players_info = online_players_info + [f"[{s}] 玩家:{len(players)} 假人:{len(bots)}",
                                                             "\n".join(["* %s"%i for i in players]),
                                                             "\n".join(["- %s"%i for i in bots])]
        online_players_info = "\n".join(online_players_info).replace("\n\n","\n").replace("\n\n","\n")
        if online_players_info[-1:] == "\n": online_players_info = online_players_info[:-1] # 修复换行问题
        QQclient.logger.info(online_players_info+"|", module_name="online-players")
        QQclient.send_msg(online_players_info, message)

@new_thread
def on_command(client, server, player, command):
    if command[:5] == "#在线玩家":
        if command == "#在线玩家":
            online_players = get_online_players(servers, server)
            online_players_info = []
            for s in online_players:
                if online_players[s] == None:
                    online_players_info = online_players_info + [f"§e[{s}] §c未运行"]
                else:
                    players = online_players[s]["players"]
                    bots = online_players[s]["bots"]
                    online_players_info = online_players_info + [f"§e[{s}] §b玩家§f:{len(players)} §d假人§f:{len(bots)}§f",
                                                                "\\n".join(["§f* §b%s"%i for i in players]),
                                                                "\\n".join(["§f- §d%s"%i for i in bots])]
            online_players_info = 'tellraw %s {"text":"%s"}'%(player,"\n".join(online_players_info).replace("\n\n","\n").replace("\n\n","\n").replace("\n","\\n"))
            if online_players_info[-2:] == "\n":
                online_players_info = online_players_info[:-2]
                server.logger.info("removed \n")
            server.logger.info(online_players_info, module_name="online-players")
            server.send_message(client, ("Server","Execute",online_players_info))
        else:
            server.logger.info("'#在线玩家' 没有需要的参数", module_name="online-players")
            server.send_message(client, ("Server","Execute", "tellraw %s '#在线玩家' 没有需要的参数"))
