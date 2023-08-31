from lazyalienws.api.data import Data

file = Data("fake_player.json")
data = file.load()

def on_command(client, server, player, command):
    if command == '#carpet':
        server.say(f'§lCarpet')
        settings = ['fakePlayerAutoReplaceTool','fakePlayerAutoReplenishment','openFakePlayerInventory','commandPlayer','accurateBlockPlacement','flippinCactus']
        for setting in settings:
            server.execute(f'carpet {setting} true')
            server.say(f'§7  {setting} -> true')
        server.say('carpet设置项修复完成')
        return True