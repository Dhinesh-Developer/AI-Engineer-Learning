

import sqlite3
from datetime import datetime

from config import DATABASE_PATH

def get_connection():
    """
    Create and return a SQLite database connection.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    return connection

def initialize_database():
    """
    Create the notes table if it does not already exist.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()

def save_note(note):
    """
    Save a note into SQLite.
    """
    connection = get_connection()
    cursor = connection.cursor()
    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO notes (note, created_at)
        VALUES (?, ?)
        """,
        (note, created_at)
    )
    connection.commit()
    note_id = cursor.lastrowid
    connection.close()
    return {
        "success": True,
        "id": note_id,
        "note": note,
        "created_at": created_at
    }


def get_all_notes():
    """
    Return all saved notes.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, note, created_at
        FROM notes
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()
    connection.close()
    return rows


def search_notes(keyword):
    """
    Search notes using a keyword.
    """

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, note, created_at
        FROM notes
        WHERE note LIKE ?
        ORDER BY id DESC
        """,
        (f"%{keyword}%",)
    )

    rows = cursor.fetchall()

    connection.close()

    return rows