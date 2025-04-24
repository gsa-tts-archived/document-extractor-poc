import boto3
from types_boto3_secretsmanager import SecretsManagerClient

from src.secret.cloud_secret_manager import CloudSecretManager
from src.secret.exception import CloudSecretManagerException


class SecretManager(CloudSecretManager):
    def __init__(self) -> None:
        self.client: SecretsManagerClient = boto3.client("secretsmanager")

    def get_secret(self, secret_id: str) -> str:
        try:
            return self.client.get_secret_value(SecretId=secret_id)["SecretString"]
        except Exception as e:
            raise CloudSecretManagerException(f"Failed to retrieve secret for {secret_id}") from e
