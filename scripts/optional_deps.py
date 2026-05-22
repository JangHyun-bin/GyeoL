from __future__ import annotations

import importlib.util


def available(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None
