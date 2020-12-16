import unittest

from ..units import add_unit, unit_update_next, generete_entrances


class TestUnits(unittest.TestCase):
    def test_add_unit(self):
        unit_a = {
            "next": {"type": "service", "id": 1},
            "unit": {"history": {}}
        }
        unit_b = {"next": "c1", "history": {}}

        self.assertEqual(
            add_unit({}, unit_a, 1),
            {1: [unit_a]}
        )

        self.assertEqual(
            add_unit({1: [unit_a]}, unit_b, 5),
            {1: [unit_a], 5: [unit_b]}
        )

    def test_unit_update_next(self):
        unit_a = {
            "next": {"type": "service", "id": 1},
            "unit": {"history": {}}
        }
        next_a = {"type": "service", "id": 1}

        self.assertEqual(
            unit_update_next(unit_a, next_a, 1),
            {
                "next": next_a,
                "unit": {
                    "history": {1: [{"type": "service", "id": 1}]}
                }
            }
        )


if __name__ == '__main__':
    unittest.main()
