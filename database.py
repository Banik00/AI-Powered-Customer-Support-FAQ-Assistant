
import sqlite3
from pathlib import Path

DB_PATH = Path("database/faq_database.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_question TEXT,
            matched_faq_id INTEGER,
            similarity_score REAL,
            response_time REAL,
            response_status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            rating INTEGER,
            comments TEXT,
            FOREIGN KEY(chat_id) REFERENCES chat_history(chat_id)
        )
    """)

    conn.commit()
    conn.close()


def save_chat(question, faq_id, score, response_time, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_history
        (user_question, matched_faq_id, similarity_score,
         response_time, response_status)
        VALUES (?, ?, ?, ?, ?)
    """, (question, faq_id, score, response_time, status))

    chat_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return chat_id


def save_feedback(chat_id, rating, comments=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (chat_id, rating, comments)
        VALUES (?, ?, ?)
    """, (chat_id, rating, comments))

    conn.commit()
    conn.close()


def get_statistics():
    conn = get_connection()

    result = conn.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN response_status = 'answered'
                THEN 1 ELSE 0 END),
            SUM(CASE WHEN response_status = 'fallback'
                THEN 1 ELSE 0 END),
            AVG(response_time)
        FROM chat_history
    """).fetchone()

    conn.close()

    return result
