"""Burrowts unit tests"""
import os
import tempfile
import threading
import unittest
from time import sleep

from burrowts import BurrowTS


class BurrowTSTests(unittest.TestCase):
    """BurrowTS unittest"""

    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(delete=False).name
        self.timeseries_db = BurrowTS(file_path=self.db_file)

    def tearDown(self) -> None:
        os.remove(self.db_file)

    def test_insert_and_retreive_series(self):
        """Test insert adn get series"""
        self.timeseries_db.insert("cpu", 10)
        self.timeseries_db.insert("cpu", 20.3)
        self.timeseries_db.insert("mem", 30.4)

        cpu = self.timeseries_db.get_series("cpu")
        mem = self.timeseries_db.get_series("mem")

        self.assertEqual(cpu, [10, 20.3])
        self.assertEqual(mem, [30.4])

    def test_thread_safety(self):
        """Test thread safety"""

        def insert_data(database: BurrowTS):
            for i in range(10):
                database.insert("series1", i)
                sleep(0.001)

        threads = []
        for _ in range(2):
            thread = threading.Thread(target=insert_data, args=(self.timeseries_db,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        series1_data = self.timeseries_db.get_series("series1")
        self.assertEqual(len(series1_data), 20)


if __name__ == "__main__":
    unittest.main()
