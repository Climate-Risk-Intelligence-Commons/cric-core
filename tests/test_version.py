"""Guards against `cric_core.__version__` drifting from `pyproject.toml`."""

import tomllib
from pathlib import Path

import cric_core


def _declared_version() -> str:
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]


def test_package_version_matches_pyproject():
    assert cric_core.__version__ == _declared_version()
