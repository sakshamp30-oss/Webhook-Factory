import sqlite3
from datetime import datetime
DB_PATH = "data/tokens.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_id TEXT,
            ip TEXT,
            user_agent TEXT,
            timestamp TEXT,
            city TEXT,
            country TEXT,
            tool TEXT,
            organisation TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_event(token_id, ip, ua, city, country, tool, organisation):
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO events(token_id, ip, user_agent, timestamp, city, country, tool, organisation) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", (token_id, ip, ua, now, city, country, tool, organisation))
    conn.commit()
    conn.close()

def get_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute(""" SELECT * FROM events ORDER BY timestamp DESC""")
    rows = cursor.fetchall()
    conn.close()
    return rows