from lazyalienws.server.core._websocket_server import LASWebsocketServer
from lazyalienws.api.decorator import new_thread
import time

def get_online_players(server: LASWebsocketServer, ignore_client: list = ["Velocity"]) -> dict:
    "return {client:[players]}"
    result_list = {}
    clients = [i for i in server.clients if i["name"] not in ignore_client]
    client_counts = len(clients)
    for client in clients:
        _get_online_players_handler(server, client, result_list)
    
    while len(result_list) < client_counts:
        time.sleep(0.1)
    
    return result_list

@new_thread
def _get_online_players_handler(server: LASWebsocketServer, client, result_list):
    try:
        result = server.create_request(client, value="list", keyword="players online")
    except Exception as e:
        server.logger.warn("Faile to create online players request. {}".format(e), warn=e)
        result = False
    if result:
        result = result.split("online: ")[1].split(", ")
    result_list[client["name"]] = result