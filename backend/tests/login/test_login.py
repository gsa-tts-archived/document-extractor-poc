from unittest import mock

import bcrypt
import pytest

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
