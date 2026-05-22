from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import shared


def load_tokens() -> dict:
    with shared.project_path("references/tokens.json").open(encoding="utf-8") as handle:
        return json.load(handle)
