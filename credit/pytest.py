import unittest
from calculator import final_amount

class TestCalculateFinalAmount(unittest.TestCase):

    def test_calculate_final_amount_zero_interest(self):
        self.assertEqual(final_amount(1000, 0, 12), 1000)

    def test_calculate_final_amount_positive_interest(self):
        self.assertAlmostEqual(final_amount(1000, 0.05, 12), 1050, places=2)

    def test_calculate_final_amount_zero_months(self):
        self.assertEqual(final_amount(1000, 0.05, 0), 1000)

if __name__ == '__main__':
    unittest.main()