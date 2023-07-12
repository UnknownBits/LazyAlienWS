help_ = '''*指令
  #帮助 -> 显示本条信息
  #今日人品 帮助 -> 今日人品帮助
  #在线玩家 -> 服务器在线玩家
  #tps #mspt -> 获取运行服务器的tps与mspt
*其他功能
  #官网 #赞助 #bluemap #status #whitelist'''

info = '''=== Lazy Alien Server ===
LAS-Bot & LAS-Plugin
版本 - v0.1.2-beta
作者 - tanh_Heng
文档 - https://docs.qq.com/doc/DRkhiSURKelBJT1BB
--- 查看帮助 #帮助 ---'''

def on_qq_message(QQclient, server, message):
    if message["message"] == "#":
        QQclient.send_msg(info, message)
    elif message["message"] == "#帮助":
        QQclient.send_msg(help_, message)
    