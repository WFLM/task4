import mysql.connector
from abc import ABCMeta, abstractmethod


class DBConnection(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, host, db_name, user, password):
        pass

    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def drop_tables(self):
        pass

    @abstractmethod
    def truncate_tables(self):
        pass

    @property
    @abstractmethod
    def connection(self):
        pass


class MySQLConnection(DBConnection):
    def __init__(self, host, db_name, user, password):
        self._connection = mysql.connector.connect(host=host, user=user, password=password)

        self._create_db_if_not_exists(db_name)
        self.create_tables()

    def __del__(self):
        self._connection.close()

    def _create_db_if_not_exists(self, db_name):
        """
        Without it we should call cursor.execute("USE [current_db]") for every new cursor.
        """
        cursor = self._connection.cursor()
        cursor.execute("SHOW DATABASES LIKE '%s'", db_name)
        if not cursor.fetchone():  # if DB doesn't exist
            cursor.execute("CREATE DATABASE %s DEFAULT CHARACTER SET 'utf8'", db_name)
        cursor.close()
        self._connection.database = db_name

    def _create_rooms_table_if_not_exists(self):
        cursor = self._connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Rooms (
        room_id INT NOT NULL,
        room_name VARCHAR(255) NOT NULL,
        PRIMARY KEY (room_id)
        )
        """)
        cursor.close()

    def _create_students_table_if_not_exists(self):
        cursor = self._connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
        student_id INT NOT NULL,
        student_name VARCHAR(255) NOT NULL,
        birthday DATE NOT NULL,
        sex ENUM('M', 'F') NOT NULL,
        room_id INT,
        PRIMARY KEY (student_id),
        FOREIGN KEY (room_id)  REFERENCES Rooms (room_id) ON DELETE CASCADE ON UPDATE CASCADE,
        INDEX (room_id),
        INDEX (birthday),
        INDEX (sex)
        )
        """)
        cursor.close()

    def create_tables(self):
        self._create_rooms_table_if_not_exists()
        self._create_students_table_if_not_exists()

    def drop_tables(self):
        cursor = self._connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS Students")
        cursor.execute("DROP TABLE IF EXISTS Rooms")
        cursor.close()

    def truncate_tables(self):
        cursor = self._connection.cursor()

        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")  # just for this cursor

        cursor.execute("SHOW TABLES LIKE 'Students'")
        if cursor.fetchone():
            cursor.execute("TRUNCATE TABLE Students")

        cursor.execute("SHOW TABLES LIKE 'Rooms'")
        if cursor.fetchone():
            cursor.execute("TRUNCATE TABLE Rooms")

        cursor.close()

    @property
    def connection(self):
        return self._connection


dbms = {"mysql": MySQLConnection}
