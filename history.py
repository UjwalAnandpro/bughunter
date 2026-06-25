import sqlite3
from datetime import datetime
import os

DB_FOLDER = "database"
DB_FILE = os.path.join(DB_FOLDER, "history.db")


class History:

    def __init__(self):

        os.makedirs(DB_FOLDER, exist_ok=True)

        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)

        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            date TEXT,

            prompt TEXT,

            command TEXT,

            output TEXT,

            analysis TEXT

        )
        """)

        self.conn.commit()

    def save(self, prompt, command, output, analysis):

        self.cursor.execute("""
        INSERT INTO history(
            date,
            prompt,
            command,
            output,
            analysis
        )
        VALUES(?,?,?,?,?)
        """, (

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            prompt,

            command,

            output,

            analysis

        ))

        self.conn.commit()

    def get_all(self):

        self.cursor.execute("""
        SELECT *
        FROM history
        ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    def delete_all(self):

        self.cursor.execute("DELETE FROM history")

        self.conn.commit()

    def close(self):

        self.conn.close()