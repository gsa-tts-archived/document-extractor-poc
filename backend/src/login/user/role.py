from abc import ABC, abstractmethod


class Role(ABC):
    @abstractmethod
    def get_role(self, principal_id: str, effect: str, resource: str) -> str:
        pass
