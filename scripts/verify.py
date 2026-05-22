from __future__ import annotations


def render_verification_available() -> bool:
    try:
        import weasyprint  # noqa: F401
        import pypdf  # noqa: F401
    except Exception:
        return False
    return True
