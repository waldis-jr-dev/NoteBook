import time
import sqlite3
from abc import ABC, abstractmethod

conn = sqlite3.connect('notes.sqlite3')
cursor = conn.cursor()
cursor.executescript('''PRAGMA foreign_keys = ON''')


class AbstractBooks(ABC):

    @abstractmethod
    def delete_book(self):
        pass

    @abstractmethod
    def book_info(self):
        pass

    @abstractmethod
    def book_content(self):
        pass

    @abstractmethod
    def change_book_name(self, new_name):
        pass


class AbstractNotes(ABC):
    @abstractmethod
    def delete_note(self):
        pass

    @abstractmethod
    def note_info(self):
        pass

    @abstractmethod
    def note_content(self):
        pass

    @abstractmethod
    def change_note_name(self, new_name):
        pass
    

class AbstractTasks(ABC):

    @abstractmethod
    def delete_task(self):
        pass

    @abstractmethod
    def task_info(self):
        pass

    @abstractmethod
    def change_task_name(self, new_name):
        pass

    @abstractmethod
    def change_task_status(self, status):
        pass


class Books(AbstractBooks):
    def __init__(self, book_name=None, book_id=None, create_new=True):
        if create_new:
            sql = '''INSERT INTO books (book_name, book_creation_time) VALUES (?,?)'''
            cursor.execute(sql, (book_name, time.time()))
            conn.commit()
            self.book_id = cursor.lastrowid
        if not create_new:
            sql = '''SELECT book_id FROM books WHERE book_id LIKE ?'''
            if len(cursor.execute(sql, (book_id,)).fetchall()) != 0:
                self.book_id = book_id
            else:
                raise KeyError('Book ID not found in DB')

    @classmethod
    def get_book_by_id(cls, book_id):
        return Books(book_id=book_id, create_new=False)

    def book_info(self):
        sql = '''SELECT book_id, book_name, book_creation_time FROM books WHERE book_id LIKE ?'''
        return cursor.execute(sql, (self.book_id,)).fetchall()

    def delete_book(self):
        sql = '''DELETE FROM books WHERE book_id LIKE ?'''
        cursor.execute(sql, (self.book_id,))
        conn.commit()
        self.book_id = None

    def book_content(self):
        sql = '''SELECT note_id FROM notes WHERE book_id LIKE ?'''
        notes = []
        for note in cursor.execute(sql, (self.book_id,)).fetchall():
            notes.append(Notes(note_id=note[0], create_new=False))
        return notes

    def change_book_name(self, new_name):
        sql = '''UPDATE books SET book_name = ? WHERE book_id LIKE ?'''
        cursor.execute(sql, (new_name, self.book_id,))
        conn.commit()

    def create_note(self, note_name):
        return Notes(note_name=note_name, book_id=self.book_id)


class Notes(AbstractNotes):
    def __init__(self, note_name=None, book_id=None, note_id=None, create_new=True):
        if create_new:
            sql = '''INSERT INTO notes (book_id, note_name, note_creation_time) VALUES (?,?,?)'''
            cursor.execute(sql, (book_id, note_name, time.time()))
            conn.commit()
            self.note_id = cursor.lastrowid
        if not create_new:
            sql = '''SELECT note_id FROM notes WHERE note_id LIKE ?'''
            if len(cursor.execute(sql, (note_id,)).fetchall()) != 0:
                self.note_id = note_id
            else:
                raise KeyError('Note ID not found in DB')

    @classmethod
    def get_note_by_id(cls, note_id):
        return Notes(note_id=note_id, create_new=False)

    def note_info(self):
        sql = '''SELECT note_id, book_id, note_name, note_creation_time FROM notes WHERE note_id LIKE ?'''
        return cursor.execute(sql, (self.note_id,)).fetchall()

    def delete_note(self):
        sql = '''DELETE FROM notes WHERE note_id LIKE ?'''
        cursor.execute(sql, (self.note_id,))
        conn.commit()
        self.note_id = None

    def note_content(self):
        sql = '''SELECT task_id FROM tasks WHERE note_id LIKE ?'''
        tasks = []
        for task in cursor.execute(sql, (self.note_id,)).fetchall():
            tasks.append(Tasks(task_id=task[0], create_new=False))
        return tasks

    def change_note_name(self, new_name):
        sql = '''UPDATE notes SET note_name = ? WHERE note_id LIKE ?'''
        cursor.execute(sql, (new_name, self.note_id,))
        conn.commit()

    def create_task(self, task_name):
        return Tasks(task_name=task_name, note_id=self.note_id)


class Tasks(AbstractTasks):
    def __init__(self, task_name=None, note_id=None, task_id=None, create_new=True):
        if create_new:
            sql = '''INSERT INTO tasks (note_id, task_name, task_creation_time) VALUES (?,?,?)'''
            cursor.execute(sql, (note_id, task_name, time.time()))
            conn.commit()
            self.task_id = cursor.lastrowid
        if not create_new:
            sql = '''SELECT task_id FROM tasks WHERE book_id LIKE ?'''
            if len(cursor.execute(sql, (task_id,)).fetchall()) != 0:
                self.task_id = task_id
            else:
                raise KeyError('Task ID not found in DB')

    @classmethod
    def get_task_by_id(cls, book_id):
        return Tasks(task_id=book_id, create_new=False)

    def delete_task(self):
        sql = '''DELETE FROM tasks WHERE task_id LIKE ?'''
        cursor.execute(sql, (self.tasks_id,))
        conn.commit()
        self.task_id = None

    def task_info(self):
        sql = '''SELECT task_id, note_id, task_name, task_creation_time, status FROM tasks WHERE task_id LIKE ?'''
        return cursor.execute(sql, (self.task_id,)).fetchall()

    def change_task_name(self, new_name):
        sql = '''UPDATE tasks SET task_name = ? WHERE task_id LIKE ?'''
        cursor.execute(sql, (new_name, self.task_id,))
        conn.commit()

    def change_task_status(self, status):
        sql = '''UPDATE tasks SET status = ? WHERE task_id LIKE ?'''
        cursor.execute(sql, (status, self.task_id))
        conn.commit()


if __name__ == '__main__':
    # homework_id = Books('Homework').book_id
    # math_id = Notes('Math', homework_id).note_id
    # ukr_id = Notes('Ukr', homework_id).note_id
    # Tasks('28.11.2020', math_id)
    # Tasks('21.11.2020', math_id)
    # Tasks('poem', ukr_id)

    book_2 = Books.get_book_by_id(2)
    print(book_2.book_info())
    for note in book_2.book_content():
        print(note.note_info())

cursor.close()
conn.close()
