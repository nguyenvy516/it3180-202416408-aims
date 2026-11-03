import unittest
from aims.dvd import DigitalVideoDisc
from aims.search import search_by_category


class TestSearch(unittest.TestCase):

    def setUp(self):
        self.dvds = [
            DigitalVideoDisc("The Lion King", "Animation", "Roger Allers", 87, 19.95),
            DigitalVideoDisc("Star Wars", "Science Fiction", "George Lucas", 87, 24.95),
            DigitalVideoDisc("Aladdin", "Animation", cost=18.99),
        ]

    def test_search_by_category(self):
        result = search_by_category(self.dvds, "animation")
        self.assertEqual(len(result), 2)
        titles = [dvd.title for dvd in result]
        self.assertIn("The Lion King", titles)
        self.assertIn("Aladdin", titles)


if __name__ == "__main__":
    unittest.main()
