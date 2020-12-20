import unittest

from ..utils import format_next, format_events


class TestUtils(unittest.TestCase):
    def test_format_next(self):
        self.assertEqual(format_next('G1'), {"type": "entrance", "id": 1})
        self.assertEqual(format_next('C2'), {"type": "service", "id": 2})
        self.assertEqual(format_next('R3'), {"type": "route", "id": 3})
        self.assertEqual(format_next('S4'), {"type": "exit", "id": 4})

    def test_format_events(self):
        self.assertEqual(
            format_events({
                "1": [
                    {"type": "entrance", "id": 1},
                    {"type": "service", "id": 1}
                ],
                "5": [{"type": "service", "id": 2}],
                "10": [{"type": "exit", "id": 1}]
            }), [
                {"at": 1, "duration": 0, "type": "entrance", "id": 1},
                {"at": 1, "duration": 4, "type": "service", "id": 1},
                {"at": 5, "duration": 5, "type": "service", "id": 2},
                {"at": 10, "type": "exit", "id": 1}
            ]
        )


if __name__ == '__main__':
    unittest.main()
