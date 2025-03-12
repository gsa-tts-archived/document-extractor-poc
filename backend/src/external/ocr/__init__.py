from abc import ABC, abstractmethod
from typing import Any


class Ocr(ABC):
    @abstractmethod
    def scan(self, s3_url: str) -> dict[str, dict[str, Any]]:
        pass


class OcrException(Exception):
    pass
