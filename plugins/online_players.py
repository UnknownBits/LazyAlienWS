from mcstatus import JavaServer
from lazyalienws.api.typing import WebsocketServerInstance, QQServerInstance
from lazyalienws.server.lib.exception import raise_exception
from lazyalienws.api.decorator import new_thread
from lazyalienws.api.data import Config
from lazyalienws.api.minecraft import get_online_players
import time

transform = Config("conf.json",filepath="").read()["websocket"]["transform"]

def on_start(server: WebsocketServerInstance):
    server.help_message.register("#在线玩家","获取各服的在线玩家与假人")

@new_thread
def on_qq_message(QQclient: QQServerInstance, server: WebsocketServerInstance, message):
    if message["message"] == "#在线玩家":
        result = get_online_players(server)
        display = []
        for client, players in result.items():
            if client in transform.keys():
                client = transform[client]["zh_cn"]
            if players == [""]:
                players = []
            if type(players) == list:
                real_players = [i for i in players if i[:5] != "[BOT]"]
                fake_players = [i[5:] for i in list(set(players) - set(real_players))]
                display.append(f"[{client}] 玩家:{len(real_players)} 假人:{len(fake_players)}")
                if real_players:
                    display.append("* "+", ".join(real_players))
                if fake_players:
                    display.append("- "+", ".join(fake_players))
            elif players == None:
                display.append(f"[{client}] 未响应请求")
            elif players == False:
                display.append(f"[{client}] 错误")
        closed_clients = list(set(transform.keys()) - set(result.keys()))
        if closed_clients:
            for client in closed_clients:
                display.append(f"[{transform[client]['zh_cn']}] 未运行")
        display = "\n".join(display)
        
        server.logger.info(display)
        QQclient.send_msg(display, message)


@new_thread
def on_command(client, server: WebsocketServerInstance, player, command):
    if command[:5] == "#在线玩家":
        if command == "#在线玩家":
            _client = client
            result = get_online_players(server)
            display = ["§e§l当前在线玩家§r"]
            for client, players in result.items():
                if client in transform.keys():
                    color = transform[client]["color"]
                    client = transform[client]["zh_cn"]
                if players == [""]:
                    players = []
                if type(players) == list:
                    real_players = [i for i in players if i[:5] != "[BOT]"]
                    fake_players = [i[5:] for i in list(set(players) - set(real_players))]
                    display.append(f"§8[§{color}{client}§8]§r §f玩家:§b{len(real_players)}§r §f假人:§7{len(fake_players)}§r")
                    if real_players:
                        display.append("* "+"§7,§r ".join(real_players))
                    if fake_players:
                        display.append("§7- "+", ".join(fake_players))
                elif players == None:
                    display.append(f"§8[§{color}{client}§8]§r §c未响应请求")
                elif players == False:
                    display.append(f"§8[§{color}{client}§8]§r §c错误")
            closed_clients = list(set(transform.keys()) - set(result.keys()))
            if closed_clients:
                for client in closed_clients:
                    color = transform[client]["color"]
                    client = transform[client]["zh_cn"]
                    display.append(f"§8[§{color}{client}§8]§r §c未运行")
            display = "\n".join(display)
            server.reply(_client, "@a", display)
        else:
            server.logger.info("'#在线玩家' 没有需要的参数", module_name="online-players")
            server.send_message(client, ("Server","Execute", "tellraw %s '#在线玩家' 没有需要的参数"))
