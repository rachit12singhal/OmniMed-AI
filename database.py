import sqlite3
import json

DB_FILE = "omnimed.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Create Patient Profiles Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER DEFAULT 25,
            gender TEXT DEFAULT 'Male'
        )
    """)
    
    # 2. Create Conversations History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            role TEXT,
            content TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    
    # Ensure at least one baseline default patient exists for our local application
    cursor.execute("SELECT COUNT(*) FROM patients")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO patients (age, gender) VALUES (25, 'Male')")
        
    conn.commit()
    conn.close()

def get_patient_profile(patient_id=1):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT age, gender FROM patients WHERE id = ?", (patient_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"age": row[0], "gender": row[1]}
    return {"age": 25, "gender": "Male"}

def update_patient_profile(age, gender, patient_id=1):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE patients SET age = ?, gender = ? WHERE id = ?", (age, gender, patient_id))
    conn.commit()
    conn.close()

def get_chat_history(patient_id=1):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM chat_history WHERE patient_id = ?", (patient_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

def save_chat_message(role, content, patient_id=1):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (patient_id, role, content) VALUES (?, ?, ?)", (patient_id, role, content))
    conn.commit()
    conn.close()

def clear_chat_history(patient_id=1):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE patient_id = ?", (patient_id,))
    conn.commit()
    conn.close()