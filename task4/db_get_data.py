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

    def _rooms_top5_min_average_age(self):
        cursor = self._db_connection.cursor()
        sql_query = """
        SELECT r.room_id, r.room_name,
               AVG(
                    (
                      (YEAR(CURRENT_DATE) - YEAR(s.birthday)) -
                      (DATE_FORMAT(CURRENT_DATE, '%m%d') < DATE_FORMAT(s.birthday, '%m%d'))
                    )
                  ) AS avg_age
        FROM Students as s, Rooms as r
        WHERE s.room_id = r.room_id
        GROUP BY s.room_id
        ORDER BY avg_age
        LIMIT 5;
        """
        cursor.execute(sql_query)
        data = cursor.fetchall()  # (id, room_name, average_age)
        cursor.close()
        return data

