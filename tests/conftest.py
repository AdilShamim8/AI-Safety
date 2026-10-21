"""Shared test configuration for the AI-Safety course repository.

The repository is a tooling-light course repo (``[tool.uv] package =
false`` in ``pyproject.toml``): the ``src/`` tree is not installed as a
distribution, so tests import it by path. This conftest puts ``src/`` on
``sys.path`` exactly once, before any test module imports
``ai_safety_course``.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
