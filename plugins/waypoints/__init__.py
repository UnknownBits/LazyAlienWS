from .control import WaypointControl
from lazyalienws.api.typing import WebsocketServerInstance

waypoint_control = WaypointControl()
WebsocketServerInstance().help_message.register("#wp","共享路径点查询")

def on_message(client, server, message):
    waypoint_control.on_message(client, server, message)

def on_command(client, server, player, command):
    waypoint_control.on_command(client, server, player, command)