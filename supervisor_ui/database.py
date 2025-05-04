import os
import sqlite3
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ai_agent", "salon_data.db"))


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS help_requests (
                    id INTEGER PRIMARY KEY,
                    customer TEXT,
                    question TEXT,
                    status TEXT DEFAULT 'pending',
                    answer TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS learned_answers (
                    id INTEGER PRIMARY KEY,
                    question TEXT UNIQUE,
                    answer TEXT
                )''')
    conn.commit()
    conn.close()

def save_request(customer, question):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO help_requests (customer, question) VALUES (?, ?)", (customer, question))
    conn.commit()
    conn.close()

def get_pending_requests():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, customer, question FROM help_requests WHERE status = 'pending'")
    rows = c.fetchall()
    conn.close()
    return rows

def resolve_request(request_id, answer):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE help_requests SET status = 'resolved', answer = ? WHERE id = ?", (answer, request_id))
    conn.commit()
    conn.close()

def get_learned_answers():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT question, answer FROM learned_answers")
    rows = c.fetchall()
    conn.close()
    return rows

def get_resolved_requests():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, customer, question, answer 
        FROM help_requests 
        WHERE status = 'resolved' AND hidden = 0
    """)
    rows = c.fetchall()
    conn.close()
    return rows


def save_learned_answer(question, answer):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO learned_answers (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()
    
def hide_request(request_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE help_requests SET hidden = 1 WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()

def delete_request(request_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM help_requests  WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()


init_db()
