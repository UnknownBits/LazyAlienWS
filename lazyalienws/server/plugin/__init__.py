from lazyalienws.server.plugin.plugin_control import PluginControl

class Plugins(PluginControl):

    def __init__(self) -> None:
        support_functions = [
            "on_message",
            "on_console",
            "on_command",
            "on_start",
            "on_return",
            "on_qq_message"
        ]
        super().__init__(support_functions)
    
    def on_message(self, client, server, message):
        self.execute(client, server, message, func="on_message")
    
    def on_console(self, server, message):
        self.execute(server, message, func="on_console")
    
    def on_command(self, client, server, player, command):
        self.execute(client, server, player, command, func="on_command")
    
    def on_return(self, client, server, message):
        self.execute(client, server, message, func="on_return")
    
    def on_start(self, server):
        self.execute(server, func="on_start")
    
    def on_qq_message(self, QQclient, server, message):
        '''on_qq_message(QQclient, server, message)'''
        self.execute(QQclient, server, message, func="on_qq_message")
    
    
    