import unittest

from ..entrance import is_entrance, generate_entrance


class TestEntrance(unittest.TestCase):
    def test_is_entrance(self):
        self.assertTrue(is_entrance("G1:2-18;C1"))
        self.assertTrue(is_entrance("G3:100-150;C1"))
        self.assertFalse(is_entrance("TS=123"))
        self.assertFalse(is_entrance("C1;1;1:4-8;C2"))

    def test_generate_entrance(self):
        self.assertEqual(
            generate_entrance("G1:2-18;C1"),
            {
                "type": "entrance",
                "id": 1,
                "min": 2,
                "max": 18,
                "next": {
                    "type": "service",
                    "id": 1
                },
            }
        )


if __name__ == '__main__':
    unittest.main()
