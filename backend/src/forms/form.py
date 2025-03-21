from abc import ABC, abstractmethod


class Form(ABC):
    @abstractmethod
    def identifier(self) -> str:
        pass

    @abstractmethod
    def form_matches(self, text: str) -> bool:
        pass

    @abstractmethod
    def queries(self) -> list[str]:
        pass
