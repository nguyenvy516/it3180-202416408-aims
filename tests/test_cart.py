import unittest
from aims.cart import Cart, MAX_NUMBERS_ORDERED
from aims.dvd import DigitalVideoDisc


class TestCart(unittest.TestCase):

    def setUp(self):
        self.cart = Cart()
        self.dvd1 = DigitalVideoDisc("The Lion King", "Animation", "Roger Allers", 87, 19.95)
        self.dvd2 = DigitalVideoDisc("Star Wars", "Science Fiction", "George Lucas", 87, 24.95)
        self.dvd3 = DigitalVideoDisc("Aladdin", "Animation", cost=18.99)

    def test_add_dvd(self):
        self.assertTrue(self.cart.add_dvd(self.dvd1))
        self.assertEqual(len(self.cart.items), 1)

    def test_add_dvd_until_full(self):
        for i in range(MAX_NUMBERS_ORDERED):
            dvd = DigitalVideoDisc(f"DVD {i}", cost=10.0)
            self.assertTrue(self.cart.add_dvd(dvd))
        self.assertEqual(len(self.cart.items), MAX_NUMBERS_ORDERED)
        extra_dvd = DigitalVideoDisc("The 21st DVD", cost=15.0)
        self.assertFalse(self.cart.add_dvd(extra_dvd))
        self.assertEqual(len(self.cart.items), MAX_NUMBERS_ORDERED)

    def test_remove_dvd(self):
        self.cart.add_dvd(self.dvd1)
        self.assertTrue(self.cart.remove_dvd(self.dvd1))
        self.assertFalse(self.cart.remove_dvd(self.dvd2))

    def test_total_cost(self):
        self.cart.add_dvd(self.dvd1)
        self.cart.add_dvd(self.dvd2)
        self.cart.add_dvd(self.dvd3)
        self.assertAlmostEqual(self.cart.total_cost(), 63.89, places=2)

    def test_discount(self):
        dvd = DigitalVideoDisc("Sample DVD", cost=100.0)
        self.cart.add_dvd(dvd)
        discounted = self.cart.total_cost_with_discount(20)
        self.assertAlmostEqual(discounted, 80.0, places=2)
        with self.assertRaises(ValueError):
            self.cart.total_cost_with_discount(150)
        with self.assertRaises(ValueError):
            self.cart.total_cost_with_discount(-5)

    def test_sort_cart(self):
        self.cart.add_dvd(self.dvd1)
        self.cart.add_dvd(self.dvd2)
        self.cart.add_dvd(self.dvd3)

        self.cart.sort_by_title()
        titles = [dvd.title for dvd in self.cart.items]
        self.assertEqual(titles, ["Aladdin", "Star Wars", "The Lion King"])

        self.cart.sort_by_cost()
        costs = [dvd.cost for dvd in self.cart.items]
        self.assertEqual(costs, [24.95, 19.95, 18.99])


if __name__ == "__main__":
    unittest.main()
