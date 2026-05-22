from __future__ import annotations


def has_placeholders(text: str) -> bool:
    return "{{" in text and "}}" in text
