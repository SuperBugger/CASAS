import importlib
import os


class PluginManager:
    def __init__(self, plugin_dir='plugins'):
        self.plugin_dir = plugin_dir
        self.plugins = {}

    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and filename != 'init.py':
                module_name = f"{self.plugin_dir}.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    plugin_class = getattr(module, 'Plugin')
                    szi_name = getattr(module.Plugin, 'SZI_NAME')
                    self.plugins[szi_name] = plugin_class()
                except (ImportError, AttributeError) as e:
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
