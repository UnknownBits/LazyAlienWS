from lazyalienws.api.data import Data
from lazyalienws.server.lib.exception import raise_exception
import datetime, time, difflib

class Waypoints:

    def __init__(self):
        self.file = Data("waypoints.json", default_data=[])
        self.data = self.file.load()
    
    def add(self, client, player, content):
        id = int(time.time()*10)
        waypoint = self._waypoint(id, client, player, content)
        if type(waypoint) != int:
            self.data.append(waypoint)
            self.file.write(self.data)
            return id
        else:
            return None
    
    def _waypoint(self, id ,client, player, content) -> dict:
        waypoint_content = content.split(":")
        waypoint_content = ":".join(waypoint_content[:-1]+[waypoint_content[-1].replace("-","_")])
        waypoint_contents = [i["waypoint"] for i in self.data]
        if waypoint_content in waypoint_contents:
            return self.data[waypoint_contents.index(waypoint_content)]["id"]
        waypoint = {
            "id": id,
            "name": content.split(":")[0],
            "client": client["name"],
            "creator": player,
            "creation_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "waypoint": waypoint_content
        }
        return waypoint

    
    def remove(self, id:int):
        waypoint = self.get_waypoint(id)
        self.data.remove(waypoint)
        waypoint["id"] = -1
        return waypoint

    def search(self, name:str, is_similar=0.5, rules="True", client=None):
        if client:
            return [i for i in self.data if (self._string_similar(name, i["name"]) >= is_similar or name in i["name"]) and i["client"] == client]
        else:
            return [i for i in self.data if self._string_similar(name, i["name"]) >= is_similar or name in i["name"]] 

    def list(self, client):
        if client:
            return [i for i in self.data if i["client"] == client]
        else:
            return self.data

    def get_waypoint(self, id:int) -> dict:
        ids = [i["id"] for i in self.data]
        if id in ids:
            return self.data[ids.index(id)]
        else:
            raise AttributeError("There is no waypoint data with id '%s'"%id)

    def edit(self, id, value):
        value = [i.split(":") for i in value]
        waypoint = self.get_waypoint(id)
        info = []
        for i in value:
            key = i[0]
            new_value = i[1]
            if key in waypoint.keys():
                if key in ["name"]:
                    waypoint[key] = new_value
                    info.append("§f标签§e'%s'§f已修改为§b'%s'§r"%(key,new_value))
                else:
                    info.append("§4标签§n'%s'§r为只读")
            else:
                info.append("§4未知标签§n'%s'")
        self.file.write(self.data)
        return info

    def _string_similar(self, string1, string2):
        return difflib.SequenceMatcher(None,string1,string2).quick_ratio()