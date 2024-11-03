import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "remission.db")
schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

with sqlite3.connect(db_path) as conn:
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
