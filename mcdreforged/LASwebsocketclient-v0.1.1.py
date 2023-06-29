from mcdreforged.api.types import PluginServerInterface, ServerInterface
import importlib

PLUGIN_METADATA = {
    'id': 'las_websocket_client',
    'version': '0.1.1',
    'name': 'LAS Websocket Client',
    'description': 'A plugin for LAS websocket server-client',
    'author': 'tanh_Heng',
    'link': 'https://lazyalienserver.top/',
    'dependencies': {
        'mcdreforged': '>=1.0.0',
    }
}

config = {
    "url":"ws://127.0.0.1:5800/",
    "client_name": None
}

default_config = config.copy()

def on_load(server: PluginServerInterface, prev_module):
    global config, client, LAS_websocket_client
    config = server.load_config_simple('config.json', default_config)
    client = None
    end = False
    if config["client_name"] == None:
        server.logger.warn("Change the client name in config.")
        server.say(r"§e[LAS-websocket-client] §c终止§f: §4必须在配置文件中设置客户端名称")
        end = True
    if end:
        return
    else:
        try:
            from lazyalienws import client
            client = client.MCDR_plugin(ServerInterface.get_instance(), config["url"], config["client_name"])
            server.logger.info("Websocket client started.")
        except Exception as e:
            raise e

def on_user_info(server, info):
    global client
    if client:
        client.on_user_info(server, info)

def on_info(server, info):
    global client
    if client:
        client.on_info(server, info)

def on_player_joined(server, player, info):
    global client
    if client:
        client.on_player_joined(server, player, info)

def on_player_left(server, player):
    global client
    if client:
        client.on_player_left(server, player)

def on_unload(server):
    global client
    if client:
        client.on_unload(server)

def on_server_startup(server):
    global client
    if client:
        client.on_server_startup(server)

def on_server_stop(server, server_return_code):
    global client
    if client:
        client.on_server_stop(server, server_return_code)