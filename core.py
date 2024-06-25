import importlib
import os
import inspect
from plugins.plugin import Plugin


class PluginManager:
    def __init__(self, plugin_dir='plugins'):
        self.plugin_dir = plugin_dir
        self.plugins = {}

    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and filename != 'init.py' and filename != 'plugin.py':
                module_name = f"{self.plugin_dir}.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    # Ищем все классы в модуле
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        # Проверяем, является ли класс подклассом Plugin, но не является самим Plugin
                        if issubclass(obj, Plugin) and obj is not Plugin:
                            plugin_instance = obj()
                            szi_name = plugin_instance.id()
                            self.plugins[szi_name] = plugin_instance
                except (ImportError, AttributeError, TypeError) as e:
                    print(f"Error loading plugin {module_name}: {e}")

    def run_plugin(self, szi_name, command, output_json=False, **kwargs):
        plugin = self.plugins.get(szi_name)
        if plugin:
            if command == "status":
                return plugin.status(json_output=output_json, **kwargs)
            elif command == "info":
                return plugin.info(json_output=output_json)
        else:
            return f"No such SZI: {szi_name}"
