from typing import Tuple, Optional
import json
from abc import ABCMeta, abstractmethod
from collections import namedtuple


class InputFilesParserError(Exception):
    pass


Room = namedtuple("Room", "room_id name")
Student = namedtuple("Student", "student_id name sex birthday room_id")


class FileParser(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, students_filename: str, rooms_filename: str) -> None:
        pass

    @abstractmethod
    def get_students(self) -> Tuple[Student, ...]:
        pass

    @abstractmethod
    def get_rooms(self) -> Tuple[Room, ...]:
        pass


class JSONParser(FileParser):
    """
    This class parses JSON-file and provides methods get_students, get_rooms.
    Files can be read once (during initialization). If data in the files is changed, a new parser object should be made.
    """
    @staticmethod
    def _get_data_using_filename(filename: str) -> dict:
        """
        This staticmethod wraps json.load function.
        The main purpose is handling exceptions related to file-opening (wrong permission etc.)
        and JSON loading (corrupted file).
        """
        try:
            with open(file=filename, mode="r") as file_handler:
                return json.load(file_handler)
        except json.JSONDecodeError as err:
            raise InputFilesParserError(f"Input file '{filename}' is corrupted. {err}")

    def __init__(self, students_filename: str, rooms_filename: str) -> None:
        self._students_filename = students_filename
        self._rooms_filename = rooms_filename

        self._students_objects: Optional[Tuple[Student, ...]] = None
        self._rooms_objects: Optional[Tuple[Room, ...]] = None

    def _parse_rooms_data(self) -> None:
        """The method is used to parse "self._rooms_data", and fills the "self._rooms_objects" with rooms."""
        rooms_data = self._get_data_using_filename(self._rooms_filename)
        self._rooms_objects = tuple(Room(room_id=room_data["id"], name=room_data["name"]) for room_data in rooms_data)

    def _parse_students_data(self) -> None:
        """
        The method is used to parse "self._students data",
        and fill Room objects from the "self._rooms_objects" dict with students.
        """
        students_data = self._get_data_using_filename(self._students_filename)
        self._students_objects = tuple(Student(student_id=student_data["id"],
                                               name=student_data["name"],
                                               sex=student_data["sex"],
                                               birthday=student_data["birthday"].split("T")[0],  # cut out unused time
                                               room_id=student_data["room"]
                                               ) for student_data in students_data)

    def get_rooms(self) -> Tuple[Room, ...]:
        if self._rooms_objects is None:
            self._parse_rooms_data()
        return self._rooms_objects

    def get_students(self) -> Tuple[Student, ...]:
        if self._students_objects is None:
            self._parse_students_data()
        return self._students_objects


parsers_for_input_files = {"json": JSONParser}
