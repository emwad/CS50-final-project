import sqlite3
from flask import g

DATABASE = "nss.db"

def get_db():
    if "db" not in g:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Function that takes an institution UKPRN, and a list of theme IDs, 
# and returns an object containing info filtered to that.

def inst(UKPRN, THEME_IDs):
    if not THEME_IDs:
        return []

    db = get_db()

    placeholders = ",".join(["?"] * len(THEME_IDs))
    query = f"SELECT * FROM nss WHERE UKPRN = ? AND THEME_ID IN ({placeholders})"

    rows = db.execute(query, (UKPRN, *THEME_IDs)).fetchall()
    return rows