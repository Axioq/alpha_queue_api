from .db import get_connection

def add_episode_progress(show_id, show_name, season, episode):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO watch_history (show_id, show_name, season, episode)
                "VALUES (%s, %s, %s, %s)
                """, (show_id, show_name, season, episode))
            conn.commit()

def get_progress_for_show(show_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT show_id, name, season, episode, watched_at
                FROM watch_history
                WHERE show_id = %s
                ORDER BY watched_at DESC
                LIMIT 1
            """, (show_id,))
            row = cur.fetchone()
            if row:
                return {
                    "show_id": row[0],
                    "name": row[1],
                    "season": row[2],
                    "episode": row[3],
                    "watched_at": row[4].isoformat()
                }
            return None

def delete_progress_for_show(show_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM watch_history WHERE show_id = %s", (show_id,))
            conn.commit()

def get_all_progress():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT show_id, name, season, episode, watched_at
                FROM watch_history
                ORDER BY watched_at DESC
            """)
            rows = cur.fetchall()
            return [
                {
                    "show_id": row[0],
                    "name": row[1],
                    "season": row[2],
                    "episode": row[3],
                    "watched_at": row[4].isoformat()
                }
                for row in rows
            ]

def insert_episode(show_id, show_name, season, episode, title, air_date):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO episodes (show_id, show_name, season, episode, title, air_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (show_id, season, episode) DO NOTHING
            """, (show_id, show_name, season, episode, title, air_date))
            conn.commit()