class DBGetData:
    def __init__(self, db_connection):
        self._db_connection = db_connection

    def _rooms_number_of_students(self):
        cursor = self._db_connection.cursor()

        sql_query = """
        SELECT r.room_id, r.room_name, COUNT(s.room_id) as num_of_students
        FROM rooms_accounting.Students as s, rooms_accounting.Rooms as r
        WHERE r.room_id = s.room_id
        GROUP BY s.room_id
        """
        cursor.execute(sql_query)
        data = cursor.fetchall()  # (id, room_name, num_of_students)
        cursor.close()
        return data
