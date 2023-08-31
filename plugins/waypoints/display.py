DIMENSION = {
    "Internal_overworld_waypoints": {
        "title_color": "dark_green",
        "pos_color": "green",
        "zh_cn": "主世界"
    },
    "Internal_the_nether_waypoints": {
        "title_color": "dark_red",
        "pos_color": "red",
        "zh_cn": "下界"
    },
    "Internal_the_end_waypoints": {
        "title_color": "dark_purple",
        "pos_color": "light_purple",
        "zh_cn": "末地"
    }
}

HELP = {
    "waypoint": [
            {"text":"§e§l【Waypoint Share】§r\n"},
            {"text":"§7#wp","clickEvent":{"action":"run_command","value":"#wp"}},
            {"text":" "},
            {"text":"§7#waypoint§f\n","clickEvent":{"action":"run_command","value":"#waypoint"}},
            {"text":"快捷使用§7(单击下方按钮)\n"},
            {"text":"[+]","color":"green",
                "clickEvent":{"action":"run_command","value":"#wp add"},
                "hoverEvent":{"action":"show_text","value":{"text":"向共享中添加坐标点\n§7#wp add"}}},
            {"text":" "},
            {"text":"[-]","color":"red",
                "clickEvent":{"action":"run_command","value":"#wp remove"},
                "hoverEvent":{"action":"show_text","value":{"text":"从共享中移除坐标点\n§7#wp remove"}}},
            {"text":" "},
            {"text":"[?]","color":"aqua",
                "clickEvent":{"action":"run_command","value":"#wp search"},
                "hoverEvent":{"action":"show_text","value":{"text":"在共享中搜索坐标点\n§7#wp search §f| §7§nXXX§r§7在哪"}}},
            {"text":" "},
            {"text":"[…]","color":"white",
                "clickEvent":{"action":"run_command","value":"#wp list"},
                "hoverEvent":{"action":"show_text","value":{"text":"列出所有共享中的坐标点\n§7#wp list"}}},
            {"text":" "},
            {"text":"[H]","color":"yellow",
                "clickEvent":{"action":"run_command","value":"#wp help"},
                "hoverEvent":{"action":"show_text","value":{"text":"查看坐标点的更多帮助\n§7#wp help"}}}
        ],
    "add": [
        {"text":"§d§l【添加坐标点】§r\n添加方式 §7(建议使用共享²)\n"},
        {"text":"共享¹","underlined":True, "color":"yellow",
            "clickEvent":{"action":"run_command","value":"#wp add share"},
            "hoverEvent":{"action":"show_text","value":{
                "text":"选择此选项后，在§n地图§r中Share(分享)需要添加的坐标点\n§7#wp add share"
            }}},
        {"text":" 选择此选项后，在§n地图§r中Share(分享)需要添加的坐标点\n"},
        {"text":"共享²","underlined":True, "color":"yellow",
            "clickEvent":{"action":"suggest_command","value":"#wp add xaero "},
            "hoverEvent":{"action":"show_text","value":{
                "text":"在§n地图§r中Share(分享)需要添加的坐标点后，单击最右端的'§a[+]§f'\n§7#wp add xaero"
            }}},
        {"text":" 单击§b§n临时坐标点§r§7(已分享但未添加的坐标点)§f最右端的'§a[+]§f'"}

    ],
    "remove": [
        {"text":"§d§l【移除坐标点】§r\n只能移除自己创建的坐标点，或需要权限"},
        {"text":"§7#wp remove <id>",
            "clickEvent":{"action":"suggest_command","value":"#wp remove "},
            "hoverEvent":{"action":"show_text","value":{"text":"单击以输入"}}}
    ],
    "search": [
        {"text":"§d§l【搜索坐标点】§r\n"},
        {"text":"§7#wp search <search>\n",
            "clickEvent":{"action":"suggest_command","value":"#wp search "},
            "hoverEvent":{"action":"show_text","value":{"text":"单击以输入"}}},
        {"text":"§7#wp search <search> --all §f搜索所有服务端的坐标点\n",
            "hoverEvent":{"action":"show_text","value":{"text":"搜索所有服务端的坐标点\n§7不只搜索此服务端的坐标点"}}},
        {"text":"§7§nXXX§r§7在哪 §f自动问答识别"}
    ],
    "edit": [
        {"text":"§d§l【修改坐标点】§r\n"},
        {"text":"§7#wp edit <id> <value1> <value2> <...>\n",
            "clickEvent":{"action":"suggest_command","value":"#wp edit "},
            "hoverEvent":{"action":"show_text","value":{"text":"单击以输入"}}},
        {"text":"§e<id> §f坐标点的唯一ID\n§e<value> §f修改值 格式为§n§7<key>:<new_value>§r §8§oname:new_name§f\n单个修改值中§c不得出现§f空格，每个修改值以空格分隔"}
    ],
    "list_all": [
        {"text":"[…]","color":"gray",
            "clickEvent":{"action":"run_command","value":"#wp list --all"},
            "hoverEvent":{"action":"show_text","value":{"text":"查看所有服务端的坐标点\n§7#wp list --all"}}},
    ]
}

# xaero_waypoint_add:tanh_Heng's Location:t:-486:64:281:6:false:0:Internal_overworld_waypoints

class WaypointDisplay:

    def waypoint_show(waypoint):
        xaero_waypoint = waypoint["waypoint"]
        id = waypoint["id"]
        dimension = DIMENSION[xaero_waypoint.split(":")[-1]]
        x, y, z = xaero_waypoint.split(":")[2:5]
        display = [
            {"text":"§e@§f §l%s§r"%waypoint["name"]},
            {"text":" §7-§f"},
            {"text":" %s"%dimension["zh_cn"],
             "color":dimension["title_color"]},
            {"text":" [%s,%s,%s]"%(int(x),int(y),int(z)),
             "color":dimension["pos_color"]},
            {"text":" "},
            {"text":"[+X]",
             "color":"gold",
             "clickEvent":{"action":"run_command", "value":"xaero_waypoint_add:%s"%xaero_waypoint},
             "hoverEvent":{"action":"show_text", "value":{"text":"添加Xaero坐标点", "color":"gold"}}},
            {"text":" "}
        ]
        if id == 0:
            display = display + [
                {"text":"[+]","color":"green",
                    "clickEvent":{"action":"run_command","value":"#wp add xaero %s"%xaero_waypoint},
                    "hoverEvent":{"action":"show_text","value":{"text":"将此坐标点添加至共享"}}},
            ]
            display[1] = {"text":" §7(临时坐标点)§f"}
        elif id != -1:
            display = display + [
                {"text":"[✎]","color":"yellow",
                    "clickEvent":{"action":"suggest_command","value":"#wp edit %s "%id},
                    "hoverEvent":{"action":"show_text","value":"§e修改坐标点信息\n§7#wp edit %s <key>:<new_value>"%id}},
                {"text":" "},
                {"text":"[…]",
                    "color":"gray",
                    "clickEvent":{"action":"run_command", "value":"#wp detail %s"%waypoint["id"]},
                    "hoverEvent":{"action":"show_text", "value":{"text":"查看坐标点详情\n§7%s§8#%s"%(waypoint["name"],waypoint["id"])}}}]
        # print("xaero_waypoint_add:%s"%xaero_waypoint)
        return display
    
    def _detail(key, value, show_text, end="\n"):
        return {"text":"  [§6%s§f] %s%s"%(key, value, end),"hoverEvent":{"action":"show_text","value":{"text":show_text}}}

    def waypoint_detail(waypoint):
        xaero_waypoint = waypoint["waypoint"]
        dimension = DIMENSION[xaero_waypoint.split(":")[-1]]
        x, y, z = xaero_waypoint.split(":")[2:5]
        id = waypoint["id"]
        display = [
            {"text":"§e§lWaypoint§f §l§b%s§r §7-§f 详情\n"%waypoint["name"]},
            WaypointDisplay._detail("ID", id, "唯一ID"),
            WaypointDisplay._detail("名称", waypoint["name"], "§e<name>§f 名称\n§7用于显示和搜索",end=""),
            {"text":" "},
            {"text":"✎\n","color":"yellow","underlined":True,
                "clickEvent":{"action":"suggest_command","value":"#wp edit %s name:"%id},
                "hoverEvent":{"action":"show_text","value":"§e修改名称\n§7#wp edit %s name:<name>"%id}},
            WaypointDisplay._detail("创建", "(%s) %s , %s"%(waypoint["client"],waypoint["creator"],waypoint["creation_time"]), "创建信息\n§7(服务端)创建者,时间"),
            WaypointDisplay._detail("维度", dimension["zh_cn"], "维度信息"),
            WaypointDisplay._detail("坐标", "%s, %s, %s"%(x,y,z), "坐标信息"),
            WaypointDisplay._detail("waypoint", xaero_waypoint, "记录的完整坐标点文本", end="")
        ]
        return display

    def waypoint_add(waypoint):
        return [{"text":"§l已添加坐标点\n"}] + WaypointDisplay.waypoint_show(waypoint)
    
    def help(key):
        if key == "help":
            return [i+[{"text":"\n"}] for i in HELP.values()][:-1]
        else:
            return HELP[key]
    
    def _get_page(string: str) -> int:
        if "page:" in string:
            start = string.index("page:") + 5
            for end in range(start, len(string)):
                if string[end] not in "0123456789":
                    break
            return int(string[start:end+1])
        else:
            return 1

    def page(command, total):
        '----- <<[  第 1/10 页 ]>> -----'
        page = WaypointDisplay._get_page(command)
        if "page:" not in command:
            command = command+" page:1"
        if page <= total:
            page_up = {"text":"<<","color":"dark_aqua","hoverEvent":{"action":"show_text","value":{"text":"上一页"}}} # 上一页
            if page <= 1:
                page_up["hoverEvent"]["value"]["strikethrough"] = True
            else:
                page_up["clickEvent"] = {"action":"run_command", "value":command.replace("page:%s"%page,"page:%s"%(page-1))}
            page_down = {"text":">>","color":"dark_aqua","hoverEvent":{"action":"show_text","value":{"text":"下一页"}}} # 下一页
            if page == total:
                page_down["hoverEvent"]["value"]["strikethrough"] = True
            else:
                page_down["clickEvent"] = {"action":"run_command", "value":command.replace("page:%s"%page,"page:%s"%(page+1))}
            display = [
                {"text":"§8-----"},
                {"text":" "},
                page_up,
                {"text":"§7[ §f第 §b%s§f/§b%s§f 页 §7]"%(page, total)},
                page_down,
                {"text":" §8-----"}
            ]
            return display
        else:
            return [{"text":"§c?会不会翻页"}]