import os
import csv
from typing import Dict, List


class CsvTable(object):
    """The CsvTable class provides a simple representation of a csv file as database table."""

    def __init__(self, name: str, column_names: List[str], data_path: str = '.') -> None:
        """
        The __init__ method for CsvTable.
        :param name: The basename of the csv file, without the .csv extension.
        :param column_names: A list containing column names.
        :param data_path: (Optional) Path to directory containing the csv file.
        """

        # Validate provided argument type
        if not isinstance(name, str):
            raise TypeError("Argument 'name' must be a str.")
        if not isinstance(column_names, list):
            raise TypeError("Argument 'column_names' must be a list.")
        if not isinstance(data_path, str):
            raise TypeError("Argument 'data_path' must be a str.")

        # Create data_path if necessary
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        # Create the full filename of the csv for this object
        self._filename = os.path.join(data_path, name + '.csv')

        # Create csv file for the table if necessary (in case of new file)
        if not os.path.exists(self._filename):
            with open(self._filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)

    def select(self, where: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Provide a simple 'select' method for the table.
        :param where: A dict describing rows to select, example: {'role': 'user', 'username': 'test_user'}.
        :return: A list of rows selected based on the provided criterion. Each row is a dict with keys taken from col_names.
        """

        # Validate provided argument type
        if not isinstance(where, dict):
            raise TypeError("Argument 'where' must be a dict.")

        # Open the csv file and filter matching records.
        matching_rows = []
        with open(self._filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            row: Dict[str, str]
            for row in reader:
                stripped_row = {key.strip(): value.strip() for key, value in row.items()}
                # Match all provided key value criteria.
                if all(stripped_row[key] == value for key, value in where.items()):
                    matching_rows.append(stripped_row)

        # Return the filtered result
        return matching_rows

    def update(self, values: Dict[str, str], where: Dict[str, str]) -> None:
        """
        Provide a simple 'update' method for the table.
        :param values: A dict describing values to update, example {'password': 'new_password'}
        :param where: A dict describing rows to select, example: {'role': 'user', 'username': 'test_user'}.
        :return: None
        """
        raise NotImplementedError('This method is not yet required for the current features.')

    def insert(self, values: Dict[str, str]) -> None:
        """
        Provide a simple 'insert' method for the table.
        :param values: A dict describing values to insert, example {'password': 'new_password'}
        :return: None
        """
        raise NotImplementedError('This method is not yet required for the current features.')

    def delete(self, where: Dict[str, str]) -> None:
        """
        Provide a simple 'delete' method for the table.
        :param where: A dict describing rows to select, example: {'role': 'user', 'username': 'test_user'}.
        :return: None
        """
        raise NotImplementedError('This method is not yet required for the current features.')
