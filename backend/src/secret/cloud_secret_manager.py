from abc import ABC, abstractmethod


class CloudSecretManager(ABC):
    @abstractmethod
    def get_secret(self, secret_id: str) -> str:
        pass
