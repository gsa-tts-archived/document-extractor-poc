from abc import ABC, abstractmethod

from src.forms.form import Form


class Ocr(ABC):
    @abstractmethod
    def extract_raw_text(self, s3_url: str) -> list[str]:
        pass

    @abstractmethod
    def scan(self, s3_url: str, queries: list[str] | None = None) -> dict[str, dict[str, str | float]]:
        pass

    @abstractmethod
    def scan_(self, s3_url: str, form: Form) -> dict[str, dict[str, str | float]]:
        pass
