from abc import ABCMeta, abstractmethod
import json
from lxml import etree  # this cython module "lxml" is used because "xml" cannot make pretty-printed files


class DataFileConstructor(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, data_sequence, data_format):
        pass

    @abstractmethod
    def construct_file(self, output_file_path):
        pass


class JSONConstructor(DataFileConstructor):
    def __init__(self, data_sequence, data_format):
        self._data_sequence = data_sequence
        self._data_format = data_format
        self._prepared_data = None

    def _prepare_data(self):
        if self._prepared_data is None:
            self._prepared_data = [dict(zip(self._data_format, data)) for data in self._data_sequence]

    def construct_file(self, output_file_path: str = "output.json"):
        self._prepare_data()

        with open(file=output_file_path, mode="w") as json_output_fh:
            json.dump(obj=self._prepared_data,
                      fp=json_output_fh,
                      indent=4
                      )
