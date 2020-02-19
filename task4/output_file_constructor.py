from abc import ABCMeta, abstractmethod
import json
from lxml import etree  # this cython module "lxml" is used because "xml" cannot make pretty-printed files
from decimal import Decimal


class DataFileConstructor(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, data_sequence, data_format):
        pass

    @abstractmethod
    def construct_file(self, output_file_path):
        pass


class DecimalEncode(json.JSONEncoder):
    """Encoding Decimal to int"""
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o)
        else:
            super().default(self, o)


class JSONConstructor(DataFileConstructor):
    def __init__(self, data_sequence, data_format):
        self._data_sequence = data_sequence
        self._data_format = data_format
        self._prepared_data = None

    def _prepare_data(self):
        if self._prepared_data is None:
            self._prepared_data = [dict(zip(self._data_format, data)) for data in self._data_sequence]

    def construct_file(self, output_file_path="output"):
        self._prepare_data()

        with open(file=f"{output_file_path}.json", mode="w") as json_output_fh:
            json.dump(obj=self._prepared_data,
                      fp=json_output_fh,
                      cls=DecimalEncode,
                      indent=4
                      )


class XMLConstructor(DataFileConstructor):
    def __init__(self, data_sequence, data_format):
        self._data_sequence = data_sequence
        self._data_format = data_format
        self._prepared_data = None

    def _make_xml_root(self):
        root_xml = etree.Element("rooms")

        for data in self._data_sequence:
            room_xml = etree.Element("room")
            root_xml.append(room_xml)

            for index, element_name in enumerate(self._data_format):
                room_element = etree.SubElement(room_xml, element_name)
                room_element.text = str(data[index])
        tree = etree.ElementTree(root_xml)
        return tree

    def construct_file(self, output_file_path="output"):
        tree = self._make_xml_root()
        tree.write(f"{output_file_path}.xml", encoding="utf-8", pretty_print=True)


format_handlers = {"json": JSONConstructor, "xml": XMLConstructor}
