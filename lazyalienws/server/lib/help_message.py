from abc import *

class HelpMessage(ABC):
    def __init__(self) -> None:
        self.help_messages = {}
    
    def register(self, command, prompt):
        self.help_messages[command] = prompt

    @abstractmethod
    def display(self):
        '''
        display help message
        '''

class HelpMessageMinecraft(HelpMessage):
    
    def display(self):
        display_msg = [[{"text":command, 
         "color":"gray",
         "hoverEvent":{"action":"show_text","value":{"text":"点击输入"}},
         "clickEvent":{"action":"suggest_command","value":command}},
         {"text":" "},
         {"text":prompt,
          "color":"white"},
         {"text":"\n"}]
         for command, prompt in self.help_messages.items()]
        display_msg[-1].remove(display_msg[-1][-1])
        display_msg = [{"text":"§e§lLazyAlienWS §r§b指令使用帮助\n"}] + display_msg
        return display_msg

class HelpMessageQQ(HelpMessage):

    def __init__(self) -> None:
        super().__init__()
        self.other_functions = []

    def register(self, command, prompt):
        if prompt:
            return super().register(command, prompt)
        else:
            self.other_functions.append(command)
    
    def display(self):
        display_msg = "\n".join([
            "=== LazyAlienWS ===",
            "QQ指令帮助",
            "\n".join(["  {} -> {}".format(command, prompt) for command, prompt in self.help_messages.items() if prompt != None]),
            "其他功能",
            "  "+" ".join(self.other_functions)])
        return display_msg
    