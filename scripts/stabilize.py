from __future__ import annotations


def normalize_hex_color(value: str) -> str:
    return value.upper() if value.startswith("#") else value
