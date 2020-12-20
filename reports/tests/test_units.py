import unittest

from ..units import get_unit_stats, get_queues_stats


class TestUnits(unittest.TestCase):
    def test_get_unit_stats(self):
        unit = {
            "id": "d40168b9-4e23-43bd-9bd6-9eef92a18b1f",
            "history": [
                {"at": 1, "duration": 0, "type": "entrance", "id": 1},
                {"at": 1, "duration": 16, "type": "service", "id": 1},
                {"at": 17, "duration": 0, "type": "route", "id": 1},
                {"at": 17, "type": "exit", "id": 1}
            ]
        }

        self.assertEqual(
            get_unit_stats(unit),
            {
                "time_spent": 16,
                "time_in_queue": 0,
                "queues": []
            }
        )

    def test_get_unit_stats_with_queue(self):
        unit = {
            "id": "03634422-f6aa-4e5f-8cb1-20e261f1edd9",
            "history": [
                {"at": 20, "duration": 0, "type": "entrance", "id": 1},
                {"at": 20, "duration": 20, "type": "service",
                    "action": "queue", "id": 1},
                {"at": 40, "duration": 20, "type": "service", "id": 1},
                {"at": 60, "type": "exit", "id": 1}
            ]
        }

        self.assertEqual(
            get_unit_stats(unit),
            {
                "time_spent": 40,
                "time_in_queue": 20,
                "queues": [
                    {"type": "service", "id": 1, "at": 20, "duration": 20}
                ]
            }
        )

    def test_get_queue_stats(self):
        unit = {
            "id": "03634422-f6aa-4e5f-8cb1-20e261f1edd9",
            "history": [
                {"at": 20, "duration": 0, "type": "entrance", "id": 1},
                {"at": 20, "duration": 20, "type": "service",
                    "action": "queue", "id": 1},
                {"at": 40, "duration": 20, "type": "service", "id": 1},
                {"at": 60, "duration": 40, "type": "service",
                    "action": "queue", "id": 2},
                {"at": 100, "type": "exit", "id": 1}
            ]
        }
        self.assertEqual(get_queues_stats(unit), [
            {'type': 'service', 'id': 1, 'at': 20, 'duration': 20},
            {'type': 'service', 'id': 2, 'at': 60, 'duration': 40},
        ])


if __name__ == '__main__':
    unittest.main()
