from array import array
import sqlite3


class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS history "
            "(id INTEGER PRIMARY KEY, date_started TIMESTAMP, time_elapsed FLOAT, records BLOB)")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def insert(self, date_started, time_elapsed, records):
        """Adds recorded information from the exercise.

        :param date_started: datetime
            Start time of recorded exercise.
        :param time_elapsed: float
            Duration of recorded exercise. Example: 5.05 (5 minutes, 5 seconds).
        :param records: list
            List of tuples, which represent each completed row from exercise.
        :return: None
        """
        script = "INSERT INTO history VALUES(NULL, ?, ?, ?)"
        # Convert list into a binary representation.
        binary_data = sqlite3.Binary(array('B', records))
        self.cur.execute(script, (date_started, time_elapsed, binary_data))
        self.conn.commit()

    def view(self):
        """Retrieve exercise information from database."""
        self.cur.execute("SELECT * FROM history")
        rows = self.cur.fetchall()
        return rows

    def delete(self, id_):
        self.cur.execute("DELETE FROM history WHERE id=?", (id_,))
        self.conn.commit()

# Get names of columns in database:
#     names = list(map(lambda x: x[0], cur.description))
#     names = [description[0] for description in cur.description]
