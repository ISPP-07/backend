from datetime import datetime, timedelta
import pytz
import json
import os
from typing import Union, Any
import bcrypt
from jose import jwt
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from src.core.config import settings
from src.core.database.backup import BackupEncoder


def create_access_token(
    subject: Union[str, Any],
    expires_delta: int = None
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(pytz.utc) + expires_delta
    else:
        expires_delta = datetime.now(pytz.utc) + timedelta(
            seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
        )
    to_encode = {"exp": expires_delta, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        settings.ALGORITHM,
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: int = None
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(pytz.utc) + expires_delta
    else:
        expires_delta = datetime.now(pytz.utc) + timedelta(
            seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS
        )

    to_encode = {"exp": expires_delta, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_REFRESH_SECRET_KEY,
        settings.ALGORITHM,
    )
    return encoded_jwt


def get_hashed_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    password_byte_enc = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_bytes)


def generate_salt() -> bytes:
    return os.urandom(16)


def derive_key(password: str, salt: bytes) -> bytes:
    key = bcrypt.kdf(password.encode(), salt,
                     desired_key_bytes=32, rounds=100)
    return key


def pad_data(data):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data


def unpad_data(data):
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(data) + unpadder.finalize()
    return unpadded_data


def encrypt_data(data, key: bytes):
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())

    encryptor = cipher.encryptor()

    padded_data = pad_data(data)

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return iv, encrypted_data


def decrypt_data(encrypted_data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())

    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding after decryption
    unpadded_data = unpad_data(decrypted_data)

    return unpadded_data
