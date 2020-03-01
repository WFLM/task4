class DBGetData:
    def __init__(self, db_connection):
        self._db_connection = db_connection

    def query_executor(self, sql_query):
        cursor = self._db_connection.cursor()  # context managers aren't implemented in this module for cursors
        cursor.execute(sql_query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def rooms_number_of_students(self):
        data_format = ("id", "room_name", "number_of_students")
        sql_query = """
        SELECT r.room_id, r.room_name, COUNT(s.room_id) AS num_of_students
        FROM rooms_accounting.Students AS s, rooms_accounting.Rooms AS r
        WHERE r.room_id = s.room_id
        GROUP BY s.room_id;
        """
        data = self.query_executor(sql_query)
        return data_format, data

    def rooms_top5_min_average_age(self):
        data_format = ("id", "room_name", "average_age")
        sql_query = """
        SELECT r.room_id, r.room_name,
               AVG(
                    (
                      (YEAR(CURRENT_DATE) - YEAR(s.birthday)) -
                      (DATE_FORMAT(CURRENT_DATE, '%m%d') < DATE_FORMAT(s.birthday, '%m%d'))
                    )
                  ) AS avg_age
        FROM Students AS s, Rooms AS r
        WHERE s.room_id = r.room_id
        GROUP BY s.room_id
        ORDER BY avg_age
        LIMIT 5;
        """
        data = self.query_executor(sql_query)
        return data_format, data

    def rooms_top5_max_age_difference(self):
        data_format = ("id", "room_name", "age_difference")
        sql_query = """
        SELECT r.room_id, r.room_name,
                MAX(
                    (
                        (YEAR(CURRENT_DATE) - YEAR(s.birthday)) - 
                        (DATE_FORMAT(CURRENT_DATE, '%m%d') < DATE_FORMAT(s.birthday, '%m%d'))
                    )
                ) -
                MIN(
                    (
                        (YEAR(CURRENT_DATE) - YEAR(s.birthday)) -
                        (DATE_FORMAT(CURRENT_DATE, '%m%d') < DATE_FORMAT(s.birthday, '%m%d'))
                    )
                ) AS age_diff
        FROM Students AS s, Rooms AS r
        WHERE s.room_id = r.room_id
        GROUP BY s.room_id
        ORDER BY age_diff DESC, s.room_id ASC
        LIMIT 5;
        """
        data = self.query_executor(sql_query)
        return data_format, data

    def rooms_with_different_sexes_students(self):
        data_format = ("id", "room_name", "males", "females")
        sql_query = """
        SELECT r.room_id, r.room_name,
               COUNT(CASE WHEN s.sex="M" THEN 1 ELSE NULL END) as M, 
               COUNT(CASE WHEN s.sex="F" THEN 1 ELSE NULL END) as F
        FROM Students AS s, Rooms AS r
        WHERE s.room_id = r.room_id
        GROUP BY s.room_id
        HAVING (COUNT(CASE WHEN s.sex="M" THEN 1 ELSE NULL END) != 0) AND 
               (COUNT(CASE WHEN s.sex="F" THEN 1 ELSE NULL END) != 0);
        """
        data = self.query_executor(sql_query)
        return data_format, data
