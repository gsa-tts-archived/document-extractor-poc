from unittest import mock

import bcrypt
import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from src import context
from src.login import login
from src.secret import CloudSecretManager, CloudSecretManagerException

context = context.ApplicationContext()


def setup_function():
    context.reset()


def test_has_valid_credentials_returns_true():
    """has_valid_credentials returns True if the credentials are valid."""

    environment = "test"
    expected_username = "DogCow"
    expected_password = "Moof"
    hashed_password = bcrypt.hashpw(expected_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    mock_cloud_secret_manager = mock.MagicMock()
    mock_cloud_secret_manager.get_secret.side_effect = (
        lambda secret_name: expected_username
        if secret_name == f"document-extractor-{environment}-username"
        else hashed_password
    )
    context.register(CloudSecretManager, mock_cloud_secret_manager)

    valid = login.has_valid_credentials(expected_username, expected_password, environment)

    assert valid is True


def test_has_valid_credentials_returns_false_for_bad_username():
    """has_valid_credentials returns False for a bad username."""

    environment = "test"
    expected_password = "Moof"
    hashed_password = bcrypt.hashpw(expected_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    mock_cloud_secret_manager = mock.MagicMock()
    mock_cloud_secret_manager.get_secret.side_effect = (
        lambda secret_name: "DogCow" if secret_name == f"document-extractor-{environment}-username" else hashed_password
    )
    context.register(CloudSecretManager, mock_cloud_secret_manager)

    valid = login.has_valid_credentials("something not correct", expected_password, environment)

    assert valid is False


def test_has_valid_credentials_returns_false_for_bad_password():
    """has_valid_credentials returns False for a bad password."""

    environment = "test"
    expected_username = "DogCow"

    mock_cloud_secret_manager = mock.MagicMock()
    mock_cloud_secret_manager.get_secret.side_effect = (
        lambda secret_name: expected_username
        if secret_name == f"document-extractor-{environment}-username"
        else bcrypt.hashpw(b"Moof", bcrypt.gensalt()).decode("utf-8")
    )
    context.register(CloudSecretManager, mock_cloud_secret_manager)

    valid = login.has_valid_credentials(expected_username, "something not correct", environment)

    assert valid is False


def test_has_valid_credentials_raises_exception_when_secret_manager_raises_exception():
    """has_valid_credentials raises an exception when the secret manager raises an exception."""

    mock_cloud_secret_manager = mock.MagicMock()
    mock_cloud_secret_manager.get_secret.side_effect = CloudSecretManagerException("something went wrong")
    context.register(CloudSecretManager, mock_cloud_secret_manager)

    with pytest.raises(CloudSecretManagerException):
        login.has_valid_credentials("DogCow", "Moof", "test")


def test_generate_token_returns_token():
    """generate_token returns a token."""

    mock_cloud_secret_manager = mock.MagicMock()
    mock_cloud_secret_manager.get_secret.return_value = generate_rsa_private_key()
    context.register(CloudSecretManager, mock_cloud_secret_manager)

    token = login.generate_token("DogCow", "test")

    assert token is not None
    assert isinstance(token, str)


def test_generate_token_raises_exception_when_secret_manager_raises_exception():
    """generate_token raises an exception when the secret manager raises an exception."""

    mock_cloud_secret_manager = mock.MagicMock()
    mock_cloud_secret_manager.get_secret.side_effect = CloudSecretManagerException("something went wrong")
    context.register(CloudSecretManager, mock_cloud_secret_manager)

    with pytest.raises(CloudSecretManagerException):
        login.generate_token("DogCow", "test")


def test_generate_token_raises_exception_when_cannot_generate_token():
    """generate_token raises an exception when JWT cannot be generated."""

    mock_cloud_secret_manager = mock.MagicMock()
    mock_cloud_secret_manager.get_secret.return_value = "not a private key"
    context.register(CloudSecretManager, mock_cloud_secret_manager)

    with pytest.raises(Exception, match="Failed to generate Token"):
        login.generate_token("DogCow", "test")


def generate_rsa_private_key() -> str:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return pem.decode("utf-8")
