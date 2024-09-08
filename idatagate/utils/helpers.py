import logging
import os
import zipfile
from typing import Optional


def get_letter(position: int) -> Optional[str]:
    if 0 <= position <= 25:
        return chr(position + 65)


def unzip(zip_path: str, extract_to: str):
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    logging.debug(f"Unzipped '{zip_path}' to '{extract_to}'")
