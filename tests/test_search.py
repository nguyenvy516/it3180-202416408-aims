import unittest
from aims.dvd import DigitalVideoDisc
from aims.search import search_by_title


class TestSearch(unittest.TestCase):

    def test_search_by_title(self):
        dvds = [DigitalVideoDisc("The Lion King")]
        result = search_by_title(dvds, "lion")
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
