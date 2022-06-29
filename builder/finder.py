from typing import Any, Optional, Union

Data = Union[str, list, dict]


class Finder:
    """
    Work recursively to either find or replace strings within a given dict or list.
    """

    data: Data
    processed_data: Data
    _found: bool = False
    _reference: str
    _references: list[str]
    _replace_with: Optional[str] = None

    def __init__(
        self,
        references: list[str],
        data: Optional[Data] = None,
        replace_with: Optional[str] = None,
    ):
        self._references = references

        if replace_with and data:
            self.replace(data, replace_with)
        elif data:
            self.found(data)

    def found(self, data: Data) -> bool:
        """
        Return a boolean result based on whether any of the
        references were found in the provided data
        """
        self._reset()
        self._search(data)
        return self._found

    def replace(self, data: Data, replace_with: Optional[str] = None) -> Data:
        """
        Find and replace all instances of all references within data
        and return updated copy of data
        """
        self._reset()
        self._replace_with = replace_with or self._replace_with
        self.processed_data = self._search(data)
        return self.processed_data

    def _reset(self):
        self._found = False

    def _search(self, data: Data) -> Data:
        for reference in self._references:
            self._reference = reference

            if isinstance(data, list):
                data = self._find_in_list(data)
            elif isinstance(data, dict):
                data = self._find_in_dict(data)

        return data

    def _find_in_str(self, data: str) -> str:
        if data in self._reference:
            self._found = True
            if self._replace_with:
                return self._replace_with

        return data

    def _find_in_list(self, data: list) -> list:
        for index, element in enumerate(data):
            if isinstance(element, str):
                data[index] = self._find_in_str(element)
            elif isinstance(element, list):
                data[index] = self._find_in_list(element)
            elif isinstance(element, dict):
                data[index] = self._find_in_dict(element)

        return data

    def _find_in_dict(self, data: dict) -> dict:
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = self._find_in_str(value)
            elif isinstance(value, list):
                data[key] = self._find_in_list(value)
            elif isinstance(value, dict):
                data[key] = self._find_in_dict(value)

        return data
