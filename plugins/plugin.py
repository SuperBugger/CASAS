from abc import ABC, abstractmethod


class Plugin(ABC):
    def __init__(self, plugin_id: str):
        self.plugin_id = plugin_id

    @abstractmethod
    def status(self, directory: str = None, json_output: bool = False) -> str:
        pass

    @abstractmethod
    def info(self, json_output: bool = False) -> str:
        pass

    @abstractmethod
    def id(self) -> str:
        pass

    @abstractmethod
    def state(self) -> str:
        pass
