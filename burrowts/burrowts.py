"""BurrowTS time series database for storing and retreiving time-stamped values"""
import os
import pickle
import time
from datetime import timedelta
from threading import Lock
from typing import Dict, List, Optional, Tuple, Union


class BurrowTS:
    """
    A time series database for storing and retreiving time-stamped values
    """

    _instance = None
    _lock = Lock()

    def __call__(self, *args, **kwargs) -> "BurrowTS":
        if not self._instance:
            self._instance = super(BurrowTS, self).__new__(*args, **kwargs)
        return self._instance

    def __init__(self, file_path: str = "burrowts.pkl") -> None:
        assert isinstance(file_path, str), "File path must be of type string."
        self.file_path = file_path
        if not os.path.isfile(self.file_path):
            self._save_data()

        self._data: Dict[str, List[Tuple[timedelta, Union[float, int]]]] = {}
        with open(self.file_path, "rb") as f:
            try:
                self._data = pickle.load(f)
            except (pickle.UnpicklingError, EOFError):
                self._data = {}

    def insert(
        self,
        series_name: str,
        value: Union[float, int],
        timestamp: Optional[timedelta] = None,
    ) -> None:
        """_summary_

        Args:
            series_name (str): time series name
            value (Union[float, int]): the value to be inserted
            timestamp (Optional[timedelta], optional): the timestamp associated with the value. Defaults to None.
        """
        assert isinstance(value, (float, int)), "Values must be of type float or int"
        if timestamp is not None:
            assert isinstance(timestamp, timedelta), "Timestamp must be of type float."

        if timestamp is None:
            timestamp = time.time()

        with self._lock:
            if series_name not in self._data:
                self._data[series_name] = []
            self._data[series_name].append((timestamp, value))
        self._save_data()

    def get_series_with_timestamp(
        self, series_name: str
    ) -> List[Tuple[timedelta, Union[float, int]]]:
        """Retrieve the time series data for a given series name.

        Args:
            series_name (str): the name of time series

        Returns:
            List[Tuple[timedelta, Union[float, int]]]: the list of values in the time series
        """
        with self._lock:
            assert (
                series_name in self._data.keys()
            ), f"Series {series_name} does not exists in the database."
            return self._data.get(series_name, [])

    def get_series(self, series_name: str) -> List[Union[float, int]]:
        """Retrieve the time series values for a given series name.

        Args:
            series_name (str): the name of time series

        Returns:
            List[Union[float, int]]: the list of values in the time series
        """
        with self._lock:
            assert (
                series_name in self._data
            ), f"Series {series_name} does not exists in the database."
            return [value for _, value in self._data[series_name]]

    def get_series_by_range(
        self, series_name: str, start_timestamp: timedelta, end_timestamp: timedelta
    ) -> List[Tuple[timedelta, Union[float, int]]]:
        """Retrieve the time series data for a given series name by range

        Args:
            series_name (str): the name of time series
            start_timestamp (timedelta): start timestamp
            end_timestamp (timedelta): end timestamp

        Returns:
            List[Tuple[timedelta, Union[float, int]]]: the list of timestamps and values tuple
        """
        with self._lock:
            assert (
                series_name in self._data
            ), f"Series {series_name} does not exists in the database."
            series_data = self._data.get(series_name, [])
            filtered_data = [
                (timestamp, value)
                for timestamp, value in series_data
                if start_timestamp <= timestamp <= end_timestamp
            ]
            return filtered_data

    def _save_data(self):
        """Save the time series to the file"""
        with self._lock:
            try:
                with open(self.file_path, "wb") as f:
                    pickle.dump(self._data, f)
            except pickle.PickleError as e:
                print(f"Error while saving data: {str(e)}")
