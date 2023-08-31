from .xaero_waypoints import Waypoints
from .display import WaypointDisplay
import re

class WaypointControl:

    def __init__(self) -> None:
        self.add_waypoint_players = []
        self.waypoints = Waypoints()
        self.PAGE_ROWS = 8
    
    def on_message(self, client, server, message):
        message = message.value
        reply = lambda string : server.reply(client, "@a", string)
        if "xaero-waypoint:" in message:
            player = message.split(">")[0][1:]
            content = ":".join(message.split("xaero-waypoint:")[1:])
            if player in self.add_waypoint_players:
                id = self.waypoints.add(client, player, content)
                self.add_waypoint_players.remove(player)
                if id:
                    reply(WaypointDisplay.waypoint_add(self.waypoints.get_waypoint(id)))
                else:
                    reply("§4添加失败: 该坐标点已存在")
            else:
                temporary_waypoint = self.waypoints._waypoint(0, client, player, content)
                if type(temporary_waypoint) != int:
                    reply(WaypointDisplay.waypoint_show(temporary_waypoint))
                else:
                    reply(WaypointDisplay.waypoint_show(self.waypoints.get_waypoint(temporary_waypoint)))
                # server.logger.info("Waypoint from %s, but the player is not in list %s"%(player, self.add_waypoint_players))
        else:
            vris = re.match(r"<[\w]+?> ([\s\S]+?)在哪里?$",message)
            if vris:
                say = lambda string: server.reply(client, "@a", string)
                name = vris.groups()[0]
                result = self.waypoints.search(name, client=client["name"])
                if len(result) > 0:
                    say("找到有关§b'%s'§f的§b%d§f个坐标点"%(name,len(result)))
                    for i in result:
                        say(WaypointDisplay.waypoint_show(i))
                else:
                    say("§4没有找到有关'%s'的坐标点 §7#wp以查看详情"%(name))
    
    def on_command(self, client, server, player, command):
        reply = lambda string: server.reply(client, player, string)
        command = command.split(" ")
        PAGE_ROWS = self.PAGE_ROWS

        if command[0] in ["#waypoint","#wp"]:

            if len(command) == 1:
                reply(WaypointDisplay.help("waypoint"))
                
            elif len(command) > 1:

                match command[1]:

                    case "help":
                        reply(WaypointDisplay.help("help"))

                    case "add":
                        if len(command) == 2:
                            reply(WaypointDisplay.help("add"))
                        if len(command) > 2:
                            if command[2] == "share":
                                self.add_waypoint_players.append(player)
                                reply("§l从Xaero World Map中分享坐标点以添加")
                            if command[2] == "xaero":
                                try:
                                    if len(command) == 4:
                                        waypoint = self.waypoints.get_waypoint(self.waypoints.add(client, player, command[3]))
                                        server.reply(client,"@a",WaypointDisplay.waypoint_show(waypoint))
                                        reply("§a添加成功")
                                    else:
                                        reply(f"§4添加失败: 未填写 xaero waypoint 信息")
                                except Exception as e:
                                    self.waypoints.remove(waypoint["id"])
                                    reply(f"§4添加失败: {e}")
                                    # reply(WaypointDisplay.help("add"))

                    case "remove":
                        if len(command) == 3:
                            id = int(command[2])
                            if player in ["tanh_Heng"] or player == self.waypoints.get_waypoint(id)["creator"]:
                                try:
                                    server.say([{"text":"§c§l坐标点已被移除§f§r "}]+WaypointDisplay.waypoint_show(self.waypoints.remove(id)))
                                except Exception as e:
                                    reply(f"§4移除失败: {e}")
                            else:
                                reply("§4移除失败: 非创建者或权限不足")
                        else:
                            reply(WaypointDisplay.help("remove"))

                    case "search":
                        if len(command) > 2:
                            if "--all" in command[-1]:
                                name = " ".join(command[2:-1])
                                search_client = None
                            else:
                                name = " ".join(command[2:])
                                search_client = client["name"]
                            reply("搜索坐标点§b'%s'§f:"%name)
                            result = self.waypoints.search(name, client=search_client)
                            if result == []:
                                reply([{"text":"§c无搜索结果 "},
                                    {"text":"[…]", "color":"gray",
                                        "hoverEvent":{"action":"show_text","value":{
                                            "text":"§f搜索所有服务端的坐标点\n§7#wp search <search> §n--all§r"
                                        }}}])
                            else:
                                command = " ".join(command)
                                page = WaypointDisplay._get_page(command)
                                start, end, total_pages = (page-1)*PAGE_ROWS, page*PAGE_ROWS, len(result)//PAGE_ROWS+1
                                if start < len(result):
                                    for i in result[start:end]:
                                        reply(WaypointDisplay.waypoint_show(i))
                                if total_pages > 1:
                                    reply(WaypointDisplay.page(command, total_pages))
                        else:
                            reply(WaypointDisplay.help("search"))
                            return
                        
                    case "detail":
                        if len(command) > 2:
                            reply(WaypointDisplay.waypoint_detail(self.waypoints.get_waypoint(int(command[2]))))
                        else:
                            reply("§c必须要指定id")
                    
                    case "list":
                        if len(command) >= 3 and "--all" in command[2:]:
                            list_client = None
                        else:
                            list_client = client["name"]
                        list_waypoints = self.waypoints.list(list_client)
                        command = " ".join(command)
                        page = WaypointDisplay._get_page(command)
                        start, end, total_pages = (page-1)*PAGE_ROWS, page*PAGE_ROWS, len(list_waypoints)//PAGE_ROWS+1
                        if start < len(list_waypoints):
                            for i in list_waypoints[start:end]:
                                try:
                                    reply(WaypointDisplay.waypoint_show(i))
                                except Exception as e:
                                    server.logger.warn("wrong waypoint info : {}".format(i), warn=e, module_name="waypoints")
                        if total_pages > 1:
                            reply(WaypointDisplay.page(command, total_pages))
                        if len(list_waypoints) == 0:
                            reply([{"text":"§c无坐标点信息"}]+WaypointDisplay.help("list_all"))

                    case "edit":
                        if len(command) > 3:
                            id = int(command[2])
                            for info in self.waypoints.edit(id, command[3:]):
                                reply(info)
                            reply(WaypointDisplay.waypoint_show(self.waypoints.get_waypoint(id)))
                        else:
                            reply(WaypointDisplay.help("edit"))

                    case _:
                        reply("§4参数错误")
                        reply(WaypointDisplay.help("waypoint"))
                

                