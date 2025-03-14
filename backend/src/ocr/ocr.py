from abc import ABC, abstractmethod


class Ocr(ABC):
    @abstractmethod
    def scan(self, s3_url: str) -> dict[str, dict[str, str | float]]:
        pass
