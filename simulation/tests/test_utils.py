import unittest

from ..utils import format_next


class TestUtils(unittest.TestCase):
    def test_format_next(self):
        self.assertEqual(format_next('G1'), {"type": "entrance", "id": 1})
        self.assertEqual(format_next('C2'), {"type": "service", "id": 2})
        self.assertEqual(format_next('R3'), {"type": "route", "id": 3})
        self.assertEqual(format_next('S4'), {"type": "exit", "id": 4})


if __name__ == '__main__':
    unittest.main()
