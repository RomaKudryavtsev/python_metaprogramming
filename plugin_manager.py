import inspect
import sys
from pathlib import Path
from importlib import import_module
from importlib import util as import_utils


class PluginManager:
    def __init__(self, plugin_dir: Path):
        self._plugins_dir = plugin_dir
        self.plugin_actions = []

    @property
    def plugins_dir(self) -> Path:
        if not self._plugins_dir.exists():
            raise FileNotFoundError(
                f"Plugin directory {self._plugins_dir} does not exist."
            )
        if not self._plugins_dir.is_dir():
            raise NotADirectoryError(f"{self._plugins_dir} is not a directory.")
        return self._plugins_dir

    def load_plugins_from_subpackages(self):
        try:
            plugins_members = inspect.getmembers(
                import_module(self.plugins_dir.name), inspect.ismodule
            )
            for name, module in plugins_members:
                if hasattr(module, "PLUGIN_ACTIONS"):
                    actions = getattr(module, "PLUGIN_ACTIONS", [])
                    self.plugin_actions.extend(actions)
                    print(f"Loaded actions from subpackage {name}: {actions}")
        except ImportError as e:
            print(f"Error loading plugins: {e}")
            raise

    def load_plugins_from_dir(self):
        for plugin_file in self.plugins_dir.glob("*.py"):
            if plugin_file.name == "__init__.py":
                continue
            module_name = plugin_file.stem
            try:
                spec = import_utils.spec_from_file_location(module_name, plugin_file)
                if spec is None:
                    print(f"Could not load spec for {module_name}. Skipping.")
                    continue
                module = import_utils.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                if hasattr(module, "PLUGIN_ACTIONS"):
                    actions = getattr(module, "PLUGIN_ACTIONS", [])
                    self.plugin_actions.extend(actions)
                    print(f"Loaded actions from file {plugin_file.name}: {actions}")
            except Exception as e:
                print(f"Error loading plugin {module_name}: {e}")

    def apply_plugin_actions(self, target_class):
        for action in self.plugin_actions:
            if action["type"] == "add_method":
                method_name = action["name"]
                method_function = action["function"]
                setattr(target_class, method_name, method_function)
                print(f"Added method {method_name} to {target_class.__name__}")


if __name__ == "__main__":
    plugin_dir = Path("plugins")
    manager = PluginManager(plugin_dir)
    manager.load_plugins_from_subpackages()
    manager.load_plugins_from_dir()
    print("Plugin manager initialized and plugins loaded.")
