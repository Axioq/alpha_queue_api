import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()  # Loads from .env into environment variables

DB_NAME = os.getenv("PG_DB")
DB_USER = os.getenv("PG_USER")
DB_PASS = os.getenv("PG_PASS")
DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)

cur = conn.cursor()

create_table_sql = """
CREATE TABLE IF NOT EXISTS watch_history (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    show_id INTEGER NOT NULL,
    season INTEGER NOT NULL,
    episode INTEGER NOT NULL,
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

cur.execute(create_table_sql)
conn.commit()

print("✅ Table 'watch_history' created or already exists.")

cur.close()
conn.close()