import datetime, copy
from lazyalienws.api.data import Data
from lazyalienws.api.typing import WebsocketServerInstance

class SignInData(Data):

    def read(self) -> dict | list:
        data = super().read()
        for index in range(len(data)):
            data[index]["latest_signin_time"] = datetime.datetime.strptime(data[index]["latest_signin_time"],'%Y-%m-%d %H:%M:%S')
        return data

    def write(self, data: dict) -> None:
        data = copy.deepcopy(data)
        for index in range(len(data)):
            data[index]["latest_signin_time"] = data[index]["latest_signin_time"].strftime("%Y-%m-%d %H:%M:%S")
        return super().write(data)

class SignIn:

    def __init__(self, server: WebsocketServerInstance) -> None:
        
        self.file = SignInData("sign_in.json",default_data=[])
        self.data = self.file.load()
        server.help_message.register("#签到","每日签到")

        try:
            self.latest_dayinfo_update_date = max([value["latest_signin_time"] for value in self.data]).date()
        except:
            server.say("[签到] §e签到信息构建完成")
            self.latest_dayinfo_update_date = datetime.datetime.now().date()

        if datetime.datetime.now().date() > self.latest_dayinfo_update_date:
            server.say("[签到] §e今日签到信息已更新")
            self.day_signin_players = [] # 当现在日期在上次更新的日期之后时，更新当日登录玩家列表
            self.latest_dayinfo_update_date = datetime.datetime.now().date()
        else:
            # if上次签到时间在今天 -> 字典{上次签到时间:玩家名} \-> 按上次签到时间排序当日登录玩家列表
            day_signin_players = {info["latest_signin_time"]:info["player"] for info in self.data if info["latest_signin_time"].date() == self.latest_dayinfo_update_date}
            self.day_signin_players = [day_signin_players[key] for key in sorted(day_signin_players)]
    
    def get_player_data(self, player:str) -> dict:
        try:
            return self.data[[i["player"] for i in self.data].index(player)]
        except:
            return None
    
    def is_player_signed_in(self, player:str) -> bool:
        player = self.get_player_data(player)
        if player:
            return player["latest_signin_time"].date() == datetime.datetime.now().date()
        else:
            return None
    
    # tanh自己忘了Message的Command是什么格式的dict了 甚至还翻了下文档（
    def sign_in(self, client, server, player, command):

        reply = lambda string: server.reply(client, player, string) 

        if command == "#签到":
            
            if datetime.datetime.now().date() > self.latest_dayinfo_update_date:
                server.say('[签到] §e今日签到信息已更新')
                self.day_signin_players = [] # 当现在日期在上次更新的日期之后时，更新当日登录玩家列表
                self.latest_dayinfo_update_date = datetime.datetime.now().date()
            
            signed_in = self.is_player_signed_in(player)
            player_data = self.get_player_data(player)

            if signed_in:

                reply(f'§7累计签到{player_data["signin_daycount"]}天 今日签到{player_data["latest_signin_time"].strftime("%H:%M:%S")}/第{self.day_signin_players.index(player)+1}位')
                reply([{"text":"§e今日已签到 "},{"text":"§d<查看今日签到详情>","clickEvent":{"action":"run_command","value":"#签到详情"},"hoverEvent":{"action":"show_text","value":{"text":"§d签到详情\n§e%s"%(datetime.datetime.now().strftime('%Y年%m月%d日'))}}}])

            else:

                if signed_in == False:
                    player_data["latest_signin_time"] = datetime.datetime.now()
                    player_data["signin_daycount"] += 1
                
                elif signed_in == None:
                    player_data = {"player":player,"latest_signin_time":datetime.datetime.now(),"signin_daycount":1}
                    self.data.append(player_data)
                
                self.day_signin_players.append(player)
                self.file.write(self.data)
            
            if not signed_in:
                text = ['',
                f'§7---- §b签到 §e{datetime.datetime.now().strftime("%Y.%m.%d")} §7----',
                f'玩家 §e{player}',
                f' - 累计签到 §e{player_data["signin_daycount"]}天',
                f' - 今日签到 §e第{len(self.day_signin_players)}位',
                f'今日首签 §e{self.day_signin_players[0]}',
                '',
                [{"text":"§e签到成功 "},{"text":"§d<查看今日签到详情>","clickEvent":{"action":"run_command","value":"#签到详情"},"hoverEvent":{"action":"show_text","value":{"text":"§d签到详情\n§e%s"%(datetime.datetime.now().strftime('%Y年%m月%d日'))}}}]]
                for t in text:
                    reply(t)
                server.say([{"text":f"[签到] 今日签到§e第{len(self.day_signin_players)}位 §b{player} "},{"text":"<点此签到>","color":"light_purple","clickEvent":{"action":"run_command","value":"#签到"},"hoverEvent":{"action":"show_text","value":{"text":"§d签到\n§e%s"%(datetime.datetime.now().strftime('%Y年%m月%d日'))}}}])
            
            return 

        elif command == "#签到详情":

            reply('')
            reply(f'§7---- §e{datetime.datetime.now().strftime("%Y年%m月%d日")} §b签到信息 §7----')
            for index, value in zip(range(len(self.day_signin_players)),[self.get_player_data(i) for i in self.day_signin_players]):
                if value["player"] == player:
                    reply(f'[第§6{index+1}§f位] §6{value["player"]} §d§f{value["latest_signin_time"].strftime("%H:%M:%S")}')
                else:
                    reply(f'[第§e{index+1}§f位] §e{value["player"]} §d§f{value["latest_signin_time"].strftime("%H:%M:%S")}')
            reply('')
            server.say([{"text":"[签到] 今日共§e%s位§f玩家已签到 "%len(self.day_signin_players)},{"text":"§d<点此签到>","clickEvent":{"action":"run_command","value":"#签到"},"hoverEvent":{"action":"show_text","value":{"text":"§d签到\n§e%s"%(datetime.datetime.now().strftime('%Y年%m月%d日'))}}}])
            
            return

def on_start(server):
    server.signin = SignIn(server)

def on_command(client, server, player, command):
    server.signin.sign_in(client, server, player, command)