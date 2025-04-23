from unittest import mock

import bcrypt

from src import context
from src.login import login
from src.secret import CloudSecretManager

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
