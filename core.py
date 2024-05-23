import importlib
import os


class PluginManager:
    def __init__(self, plugin_dir='plugins'):
        self.plugin_dir = plugin_dir
        self.plugins = {}

    def load_plugins(self):
        for plugin in os.listdir(self.plugin_dir):
            if plugin.endswith('.py') and plugin != '__init__.py':
                module_name = f"{self.plugin_dir}.{plugin[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    plugin_class = getattr(module, 'Plugin')
                    self.plugins[plugin[:-3]] = plugin_class
                except (ImportError, AttributeError) as e:
                    print(f"Error loading plugin {module_name}: {e}")

    def run_plugins(self):
        results = {}
        for name, plugin in self.plugins.items():
            results[name] = plugin.run(plugin)
        return results

    def list_plugins(self):
        for plugin in self.plugins:
            print(plugin)

