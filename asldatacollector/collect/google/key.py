import json
import os
from typing import Optional

from cryptography.fernet import Fernet
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def decode(encoded_str: str, key: str) -> str:
    """Decrypt the encoded JSON string using the provided key."""
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encoded_str.encode())
    return decrypted_message.decode()


def get_key(key_flag: Optional[str], key_file: str) -> bytes:
    """Retrieve the encryption key from a flag or a file."""
    if key_flag:
        return key_flag.encode()
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            return f.read().strip().encode()
    raise ValueError(
        "Encryption key is required. Provide it via --key flag or key.txt file."
    )


def get_service_account_credentials(
    service_account_file: str, key: bytes
) -> Credentials:
    """Decrypt the service account JSON file and return credentials."""
    with open(service_account_file, "r") as f:
        encrypted_data = f.read()
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data.encode())
    service_account_info = json.loads(decrypted_data)
    return Credentials.from_service_account_info(
        service_account_info, scopes=["https://www.googleapis.com/auth/drive.file"]
    )


def get_drive_service(creds: Credentials):
    """Return a Google Drive service instance."""
    return build("drive", "v3", credentials=creds)


def initialize_service(key_flag: Optional[str]):
    """Initialize the Google Drive service."""
    key_file = "key.txt"
    key_bytes = get_key(key_flag, key_file)
    service_account_file = os.path.join(
        os.path.dirname(__file__), "..", "..", "assets", "encsa.txt"
    )
    creds = get_service_account_credentials(service_account_file, key_bytes)
    return get_drive_service(creds)
