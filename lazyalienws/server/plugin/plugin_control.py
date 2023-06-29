import os, time
from lazyalienws.server.plugin.plugin import Plugin
from lazyalienws.server.plugin.plugin_mixin import PluginMixin

class PluginControl(PluginMixin):

    def __init__(self, support_functions=[]) -> None:
        items = [i for i in os.scandir("plugins")]
        items = [".".join(i.path[8:].split(".")[:-1]) for i in items if i.is_file()] + [i.path[8:] for i in items if i.is_dir() and "__pycache__" not in i.path]
        self.plugins = {i:Plugin(i) for i in items if i != ""}
        for plugin in self.plugins.values():
            plugin.load()
        self.mixin(support_functions)
    
    def list(self, is_loaded=None) -> list:
        if is_loaded == None:
            return self.plugins.keys()
        elif is_loaded == True:
            return [i for i in self.plugins.keys() if self.plugins[i].is_loaded]
        elif is_loaded == False:
            return [i for i in self.plugins.keys() if not self.plugins[i].is_loaded]

    def load(self, id: str):
        self.plugins[id].load()
    
    def unload(self, id: str):
        self.plugins[id].unload()
    
    def reload(self, id: str):
        self.plugins[id].reload()