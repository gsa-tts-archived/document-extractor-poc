from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def something(self):
        pass
