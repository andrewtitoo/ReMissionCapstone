import sqlite3
import os

# Path to the remission.db database file
db_path = os.path.join(os.path.dirname(__file__), "remission.db")
# Path to the schema.sql file to define the database structure
schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

with sqlite3.connect(db_path) as conn:
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
