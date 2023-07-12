import datetime
from random import randint

special_thanks = ['RCY_QWQ', '404zero', 'HuskyNB', 'xephyrs', 'Fanzhitianyu', 's_m_l', 'typo', 'ZiEric', '0UIOmc0', 'typogalaxies1122']

def JOINmotd(client, server, player):

    reply = lambda string: server.reply(client, player, string)
    signin = server.signin

    now_time = datetime.datetime.now()
    server_days = (now_time - datetime.datetime.strptime('2022-08-29','%Y-%m-%d')).days

    for i in ['',
                '§7=======§f 欢迎来到 §3§k§lI§r§b§lLazy-Alien-Server§3§k§lI§r§f §7=======',
                f'今天是§eLAS§c§f开服的第§e§l{server_days}§f天']:
        reply(i)
    website = ["§b[官网] §f打开官网 ",{ "text":"<LAS官网>","color":"light_purple","clickEvent":{"action":"open_url","value":"https://lazyalienserver.top"},"hoverEvent":{"action":"show_text","value":{"text":"打开§bLAS官网\n§7lazyalienserver.top"}}}]
    if not signin.is_player_signed_in(player):
        signin = [{"text":"§b[签到] §f签到 "},{"text":"<点此签到>","color":"light_purple","clickEvent":{"action":"run_command","value":"#签到"},"hoverEvent":{"action":"show_text","value":{"text":"§d签到\n§e%s"%(datetime.datetime.now().strftime('%Y年%m月%d日'))}}}]
    else:
        signin = {"text":"§b[签到] §f今日已签到"}
    command_help = [{"text":"§b[帮助] §f查看LAS插件帮助 "},{"text":"<查看帮助>","color":"light_purple","clickEvent":{"action":"run_command","value":"#"},"hoverEvent":{"action":"show_text","value":{"text":"快捷指令 §e#"}}}]
    reply(website)
    reply(command_help)
    reply(signin)

    if player not in special_thanks:
        join_special_thanks = [{"text":f"§6[特别鸣谢] §f{' / '.join(special_thanks)}  "},{"text":"加入赞助","color":"gray","underlined":True,"italic":True,"clickEvent":{"action":"open_url","value":"https://afdian.net/a/tanh_Heng"},"hoverEvent":{"action":"show_text","value":{"text":"打开§b爱发电赞助\n§7afdian.net/a/tanh_Heng"}}}]
        reply(join_special_thanks)

    reply('')
    hour = now_time.hour

    if player in special_thanks:
        fix = ('','  §6感谢您的赞助')
    elif player == 'tanh_Heng':
        fix = ('§3§k§lI§r§b',' 物理服主§3§k§lI§r§b')
    elif player == 'CatCoinZHSM':
        fix = ('§3§k§lI§r§b',' 服主§3§k§lI§r§b')
    else:
        fix = ('','')

    if (hour <= 3) or (hour >= 22):
        welcome = ['夜已深','早些休息','欢迎回来'][randint(0,2)]
    elif hour < 11:
        welcome = ['早上好','早安','欢迎回来'][randint(0,2)]
    elif hour < 14:
        welcome = ['中午好','午安','欢迎回来'][randint(0,2)]
    elif hour < 18:
        welcome = ['下午好','欢迎回来'][randint(0,1)]
    else:
        welcome = ['晚上好','欢迎回来'][randint(0,1)]
    server.reply(client,"@a",f'{fix[0]}{welcome}, {player}{fix[1]}')

def on_command(client, server, player, command):
    if command == "#LAS":
        JOINmotd(client, server, player)