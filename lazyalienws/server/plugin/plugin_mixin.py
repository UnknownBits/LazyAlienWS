from lazyalienws.server.lib.exception import raise_exception

class PluginMixin:

    def mixin(self, support_functions=[]) -> None:
        plugins = self.plugins
        self.mixin_dictionary = {func:[] for func in support_functions}
        for plugin_id in plugins.keys():
            plugin = plugins[plugin_id]
            for func in support_functions:
                if func in plugin.funcdir:
                    self.mixin_dictionary[func].append(plugin_id)
    
    def execute(self, *args, func: str):
        if func in self.mixin_dictionary.keys():
            for plugin_id in self.mixin_dictionary[func]:
                self.plugins[plugin_id].execute(*args, func=func)
        else:
            raise_exception(AttributeError("Unknown function name : %s"%func))  