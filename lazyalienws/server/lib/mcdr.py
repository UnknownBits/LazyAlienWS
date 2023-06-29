import json

class MCDR_API:

    def say(self, string):
        if type(string) not in [dict,list]:
            string = {"text":string}
        string = json.dumps(string)
        self.send_message_to_all_except("QQ",("Server","Execute","tellraw @a "+string))
    
    def execute(self, string):
        self.send_message_to_all_except("QQ",("Server","Execute",string))
    
    def reply(self, client, player, string):
        if type(string) not in [dict,list]:
            string = {"text":string}
        string = json.dumps(string)
        self.send_message(client, ("Server","Execute",'tellraw %s %s'%(player,string)))