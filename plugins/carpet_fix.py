from lazyalienws.api.data import Data

file = Data("fake_player.json")
data = file.load()

def on_command(client, server, player, command):
    if command == '#carpet':
        server.say(f'§lCarpet')
        settings = ['fakePlayerAutoReplaceTool','fakePlayerAutoReplenishment','openFakePlayerInventory','commandPlayer']
        for setting in settings:
            server.execute(f'carpet {setting} true')
            server.say(f'§7  {setting} -> true')
        server.say('carpet设置项修复完成')
        return True
    elif command[:7] == "#player":
        global file
        if player in data.keys():
            server.reply(client, player, "§e你已经召唤了一次无前缀假人了")
        else:
            server
        