from abc import ABC, abstractmethod
from typing import Any


class Database(ABC):
    @abstractmethod
    def get_document(self, document_id: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def write_document(self, document: dict[str, Any]):
        pass
