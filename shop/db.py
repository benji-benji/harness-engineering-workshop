import os
import sqlite3
from pathlib import Path

MIGRATIONS = Path(__file__).resolve().parent.parent / "migrations"


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(os.environ.get("SHOP_DB", "shop.db"))
    connection.row_factory = sqlite3.Row
    for migration in sorted(MIGRATIONS.glob("*.sql")):
        connection.executescript(migration.read_text())
    return connection
