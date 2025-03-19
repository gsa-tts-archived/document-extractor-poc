from abc import ABC, abstractmethod


class Ocr(ABC):
    @abstractmethod
    def detect_document_type(self, s3_url: str) -> str | None:
        pass

    @abstractmethod
    def scan(self, s3_url: str) -> dict[str, dict[str, str | float]]:
        pass
