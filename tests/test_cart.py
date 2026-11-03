import unittest
from aims.cart import Cart, MAX_NUMBERS_ORDERED
from aims.dvd import DigitalVideoDisc


class TestCart(unittest.TestCase):

    def setUp(self):
        self.cart = Cart()

    def test_add_dvd_until_full(self):
        for i in range(MAX_NUMBERS_ORDERED):
            dvd = DigitalVideoDisc(f"DVD {i}", cost=10.0)
            self.assertTrue(self.cart.add_dvd(dvd))
        self.assertEqual(len(self.cart.items), MAX_NUMBERS_ORDERED)
        extra_dvd = DigitalVideoDisc("The 21st DVD", cost=15.0)
        # Should return False when cart is full
        self.assertFalse(self.cart.add_dvd(extra_dvd))
        self.assertEqual(len(self.cart.items), MAX_NUMBERS_ORDERED)


if __name__ == "__main__":
    unittest.main()
