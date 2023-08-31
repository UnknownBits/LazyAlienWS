from mcdreforged.api.all import PluginServerInterface, ServerInterface, SimpleCommandBuilder
from lazyalienws import client
from lazyalienws.constants.client_constants import CONFIG

default_config = CONFIG.copy()
CLIENT = None

def start(server):
    global CLIENT
    config = server.load_config_simple('config.json', default_config)
    CLIENT = None
    if config["client_name"] == None:
        server.logger.warn("Change the client name in config.")
        server.say(r"§e[LazyAlienWS] §c终止§f: §4必须在配置文件中设置客户端名称")
        return
    else:
        try:
            CLIENT = client.MCDR_plugin(ServerInterface.get_instance(), config["url"], config["client_name"])
            server.logger.info("Websocket client started.")
        except Exception as e:
            raise e

def on_load(server: PluginServerInterface, prev_module):
    start(server)
    server.register_help_message("#","LazyAlienWS插件使用帮助")
    builder = SimpleCommandBuilder()
    builder.command("!!lazyalienws reload",start)
    builder.register(server)

def on_user_info(server, info):
    if CLIENT:
        CLIENT.on_user_info(server, info)

def on_info(server, info):
    if CLIENT:
        CLIENT.on_info(server, info)

def on_player_joined(server, player, info):
    if CLIENT:
        CLIENT.on_player_joined(server, player, info)

def on_player_left(server, player):
    if CLIENT:
        CLIENT.on_player_left(server, player)

def on_unload(server):
    if CLIENT:
        CLIENT.on_unload(server)

def on_server_startup(server):
    if CLIENT:
        CLIENT.on_server_startup(server)

def on_server_stop(server, server_return_code):
    if CLIENT:
        CLIENT.on_server_stop(server, server_return_code)