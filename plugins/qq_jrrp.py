import random, json
from datetime import date
import time
from lazyalienws.api.data import Data

def luck_simple(num):
    if num < 16:
        return ('大吉','万事如意，一帆风顺 ~')
    elif num < 33:
        return ('吉','今天是幸运的一天！')
    elif num < 50:
        return ('末吉','每日小幸运(1/1)')
    elif num < 66:
        return ('末凶','好像有点小问题？')
    elif num < 83:
        return ('凶','嘶……问题不大(?)')
    else:
        return ('大凶','开溜(逃)')

class LuckSentence:

    def __init__(self, filepath="LAS-websocket-server/data/luck_sentence.json") -> None:
        self.file = Data("luck_sentence.json")
        self.sentences = self.file.load()
    

    def get_luck_sentence(self, lucknum):
        rnd = random.Random()
        rnd.seed(int(date.today().strftime("%y%m%d")) + lucknum + random.randint(0,min(2,len(self.sentences)-1)))
        if len(self.sentences) > 0:
            index = rnd.randint(0,len(self.sentences)-1)
            return self.sentences[index]
        else:
            return None

    def add(self, sender, sentence, sentence_from):
        self.sentences.append({"sender":sender,"sentence":sentence,"from":sentence_from})
        self.file.write(self.sentences)
    
    def delete(self, sentence_dict):
        self.sentences.remove(sentence_dict)
        self.file.write(self.sentences)
        

luck_sentence = LuckSentence()

def on_qq_message(QQclient, server, message):
    content = message["message"].replace("\r\n","\n")

    # jrrp
    if content == "#今日人品" :
        rnd = random.Random()
        rnd.seed(int(date.today().strftime("%y%m%d"))+int(message["sender"]["user_id"]))
        lucknum = rnd.randint(0,100)
        lucksimple = luck_simple(lucknum)
        lucksentence = luck_sentence.get_luck_sentence(lucknum)
        if lucksentence != None:
            sender = lucksentence["sender"]
            lucksentence = "「%s」\n    ——%s"%(lucksentence["sentence"],lucksentence["from"])
        else:
            sender = "?"
            lucksentence = "快点使用#今日人品 投稿！！！"
        msg = f'''[CQ:reply,id={message["message_id"]}]=====『{lucksimple[0]}』=====
* 幸运指数 : {100-lucknum}%
{lucksimple[1]}
- - - - - - - - - - - - - - - -
{lucksentence}
---[ from {sender} ]---
#今日人品 #今日人品 帮助'''

    # luck-sentence
    elif content[:8] == "#今日人品 投稿":
        if len(content) == 8:
            msg = '''投稿格式: 
#今日人品 投稿
!文本
在此处填写文本 可换行
!出处
在此处填写出处 作者《出处》'''
        else:
            if "!文本\n" in content and "!出处\n"in content:
                try:
                    sentence = content.split("\n!出处\n")[0].split("!文本\n")[1]
                    sentence_from = content.split("!出处\n")[1]
                    luck_sentence.add(message["sender"]["user_id"],sentence, sentence_from)
                    QQclient.logger.info("Added luck-sentence",module_name="luck-sentence")
                    msg = '''投稿成功:
「%s」
    ——%s'''%(sentence, sentence_from)
                except Exception as e:
                    QQclient.logger.warn("Failed to add luck-sentence",warn=e,module_name="luck-sentence")
                    msg = '''投稿失败'''
            else:
                msg = '''参数错误'''
    
    # luck-sentence del
    elif content == "#今日人品 撤回投稿":
        sender = message["sender"]["user_id"]
        sentence = None
        for sentence in luck_sentence.sentences[::-1]:
            if sentence["sender"] == sender:
                break
        if sentence != None:
            luck_sentence.delete(sentence)
            msg = '''撤回成功:
「%s」
    ——%s'''%(sentence["sentence"], sentence["from"])
        else:
            msg = '''撤回失败:找不到可以撤回的消息'''
    
    # jrrp help
    elif content == "#今日人品 帮助":
        msg = '''今日人品
#今日人品 -> 今日幸运指数+语录(娱乐向)
——语录每人每日至多随机三句(但是有新投稿就会刷新 特性!)
#今日人品 投稿 -> 查看如何投稿语录
#今日人品 撤回投稿 -> 撤回自己的上一条投稿
#今日人品 帮助 -> 显示此信息'''
    else:
        return 
    
    QQclient.send_msg(msg, message)