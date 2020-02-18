class DBFill:
    def __init__(self, db_connection, rooms_objects, students_objects):
        self._connection = db_connection
        self._rooms_objects = rooms_objects
        self._students_objects = students_objects

    def _fill_rooms(self):
        cursor = self._connection.cursor()
        sql_query = "INSERT INTO Rooms(room_id, room_name) VALUES (%s, %s)"
        cursor.executemany(sql_query, self._rooms_objects)
        self._connection.commit()
        cursor.close()

    def _fill_students(self):
        cursor = self._connection.cursor()
        sql_query = "INSERT INTO Students(student_id, student_name, sex, birthday, room_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(sql_query, self._students_objects)
        self._connection.commit()
        cursor.close()

    def fill_db(self):
        self._fill_rooms()
        self._fill_students()
