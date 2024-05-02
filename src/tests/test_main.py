import unittest

from src.main import add_numbers # Assuming function is in src/main.py

class TestMain(unittest.TestCase):

    def test_add_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5, "Should be 5")

if __name__ == '__main__':
    unittest.main()