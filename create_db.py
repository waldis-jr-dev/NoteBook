import sqlite3

conn = sqlite3.connect('notes.sqlite3')
cursor = conn.cursor()

cursor.executescript('''CREATE TABLE IF NOT EXISTS books (
                            book_id INTEGER UNIQUE PRIMARY KEY NOT NULL,
                            book_name TEXT NOT NULL,
                            book_creation_time INTEGER NOT NULL)''')

cursor.executescript('''CREATE TABLE IF NOT EXISTS notes (
                            note_id INTEGER UNIQUE PRIMARY KEY NOT NULL,
                            book_id INTEGER NOT NULL, 
                            note_name TEXT NOT NULL,
                            note_creation_time INTEGER NOT NULL,
                            FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE)''')

cursor.executescript('''CREATE TABLE IF NOT EXISTS tasks (
                            task_id INTEGER UNIQUE PRIMARY KEY NOT NULL,
                            note_id INTEGER NOT NULL, 
                            task_name TEXT NOT NULL,
                            task_creation_time INTEGER NOT NULL,
                            status INTEGER NOT NULL DEFAULT 0,
                            FOREIGN KEY(note_id) REFERENCES notes(note_id) ON DELETE CASCADE ON UPDATE CASCADE)''')

cursor.close()
conn.close()
