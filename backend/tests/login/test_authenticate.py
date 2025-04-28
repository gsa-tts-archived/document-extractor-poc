import datetime
from unittest import mock

import jwt
import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from src import context
from src.login import authenticate
from src.secret import CloudSecretManager, CloudSecretManagerException

context = context.ApplicationContext()


def setup_function():
    context.reset()


def test_has_valid_token_returns_true():
    public_key, private_key = generate_rsa_public_private_key_pair()
    token = generate_token(private_key)
    mock_cloud_secret_manager = mock.MagicMock()
    mock_cloud_secret_manager.get_secret.return_value = public_key
    context.register(CloudSecretManager, mock_cloud_secret_manager)

    has_valid_token = authenticate.has_valid_token(token, "test")

    assert has_valid_token


def test_has_valid_token_returns_false_with_bad_token():
    public_key, private_key = generate_rsa_public_private_key_pair()
    mock_cloud_secret_manager = mock.MagicMock()
    mock_cloud_secret_manager.get_secret.return_value = public_key
    context.register(CloudSecretManager, mock_cloud_secret_manager)

    has_valid_token = authenticate.has_valid_token("bad_token", "test")

    assert not has_valid_token


def test_has_valid_token_returns_false_with_bad_secret():
    public_key, private_key = generate_rsa_public_private_key_pair()
    token = generate_token(private_key)
    mock_cloud_secret_manager = mock.MagicMock()
    mock_cloud_secret_manager.get_secret.return_value = "super_duper_secrets_are_just_legend"
    context.register(CloudSecretManager, mock_cloud_secret_manager)

    has_valid_token = authenticate.has_valid_token(token, "test")

    assert not has_valid_token


def test_has_valid_token_returns_null_secret_raises_exception():
    public_key, private_key = generate_rsa_public_private_key_pair()
    token = generate_token(private_key)
    mock_cloud_secret_manager = mock.MagicMock()
    mock_cloud_secret_manager.get_secret.side_effect = CloudSecretManagerException("something went wrong")
    context.register(CloudSecretManager, mock_cloud_secret_manager)

    with pytest.raises(CloudSecretManagerException):
        authenticate.has_valid_token(token, "test")


def test_generate_role_returns_deny_role():
    pass


def generate_rsa_public_private_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return public_pem.decode("utf-8"), private_pem.decode("utf-8")


def generate_token(private_key):
    try:
        payload = {"sub": "username", "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)}
        return jwt.encode(payload, private_key, algorithm="RS512")
    except Exception as e:
        print(f"Unable to generate token: {e}")
