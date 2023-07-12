from .control import WaypointControl

waypoint_control = WaypointControl()

def on_message(client, server, message):
    waypoint_control.on_message(client, server, message)

def on_command(client, server, player, command):
    waypoint_control.on_command(client, server, player, command)