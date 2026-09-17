from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def temporary_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHOP_DB", str(tmp_path / "shop.db"))
