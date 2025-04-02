from abc import ABC, abstractmethod


class CloudStorage(ABC):
    @abstractmethod
    def file_exists_and_allowed_to_access(self, remote_url: str) -> bool:
        pass

    @abstractmethod
    def access_url(self, remote_url: str) -> str:
        pass

    @abstractmethod
    def get_file(self, remote_url: str) -> bytes:
        pass

    @abstractmethod
    def put_object(self, bucket_name: str, key: str, body: bytes, metadata: dict[str, str]):
        pass
