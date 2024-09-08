from typing import Optional


def get_letter(position: int) -> Optional[str]:
    if 0 <= position <= 25:
        return chr(position + 65)
