import importlib, sys
from lazyalienws.server.lib.exception import raise_exception

class Plugin:

    def __init__(self, file) -> None:
        self.file = file
        self.is_loaded : bool = False
        self.is_imported : bool = False
        self._import()

    def _import(self):
        try:
            self.plugin = importlib.import_module(".%s"%self.file, "plugins") # 按文件import
            self.is_imported = True
            self.funcdir = [i for i in self.plugin.__dir__() if i[:3] != "__" and i[-2:] != "__"]
        except Exception as e:
            self.plugin = None
            self.is_imported = False
            self.funcdir = []
            raise_exception(e)
            
    
    def load(self):
        if self.is_imported:
            self.is_loaded = True
            return True
        else:
            return False
    
    def unload(self):
        if self.is_loaded:
            self.is_loaded = False
            return True
        else:
            return None
    
    def reload(self):
        if self.is_imported:
            self.is_loaded = False
            del sys.modules["plugins.%s"%self.file] # 重载 删除旧的import
            self._import()
            if self.plugin:
                self.is_loaded = True
        else:
            self._import()
    
    def execute(self, *args, func: str):
        "plugin.func(*args)"
        if self.is_loaded:
            try:
                eval("self.plugin.%s(*args)"%func)
            except Exception as e:
                raise_exception(e)
