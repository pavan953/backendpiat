import sqlite3
from datetime import datetime

def create_connection():
    return sqlite3.connect('person_database.db')

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            usn TEXT PRIMARY KEY,
            name TEXT,
            face_encoding BLOB,
            last_recognized TEXT,
            face_image BLOB
        )
    ''')
    conn.commit()
    conn.close()

def add_person(usn, name, face_encoding, face_image):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO persons (usn, name, face_encoding, last_recognized, face_image)
        VALUES (?, ?, ?, ?, ?)
    ''', (usn, name, face_encoding, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), face_image))
    conn.commit()
    conn.close()

def update_last_recognized(usn, face_image):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE persons
        SET last_recognized = ?, face_image = ?
        WHERE usn = ?
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), face_image, usn))
    conn.commit()
    conn.close()

def get_all_persons():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT usn, name, face_encoding  FROM persons')
    persons = cursor.fetchall()
    conn.close()
    return persons

def get_person_by_usn(usn):
    """
    Retrieve a person from the database by their USN.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM persons WHERE usn = ?', (usn,))
    person = cursor.fetchone()
    conn.close()
    return person

def create_tracking_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracking (
            usn TEXT PRIMARY KEY,
            name TEXT,
            face_image BLOB,
            last_seen TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracking_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usn TEXT NOT NULL,
            camera_id TEXT NOT NULL,
            face_image BLOB,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usn) REFERENCES persons(usn)
        )
    ''')
    conn.commit()
    conn.close()

def update_tracking(usn, name, face_image):
    """
    Update tracking information for a person.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE persons
        SET last_recognized = ?, face_image = ?
        WHERE usn = ?
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), face_image, usn))
    conn.commit()
    conn.close()

def add_tracking_event(usn, camera_id, face_image):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tracking_events (usn, camera_id, face_image) VALUES (?, ?, ?)', 
                (usn, camera_id, face_image))
    conn.commit()
    conn.close()

def get_tracking_history(usn=None):
    conn = create_connection()
    cursor = conn.cursor()
    if usn:
        cursor.execute('''
            SELECT t.*, p.name 
            FROM tracking_events t 
            JOIN persons p ON t.usn = p.usn 
            WHERE t.usn = ? 
            ORDER BY t.timestamp DESC''', (usn,))
    else:
        cursor.execute('''
            SELECT t.*, p.name 
            FROM tracking_events t 
            JOIN persons p ON t.usn = p.usn 
            ORDER BY t.timestamp DESC''')
    events = cursor.fetchall()
    conn.close()
    return events

create_table()
create_tracking_table()