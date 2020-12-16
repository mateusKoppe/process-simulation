import unittest

from ..duration import is_duration, generate_duration


class TestDuration(unittest.TestCase):
    def test_is_duration(self):
        self.assertTrue(is_duration("TS=230"))
        self.assertTrue(is_duration("TS=200"))
        self.assertFalse(is_duration("G1:2-18;C1"))
        self.assertFalse(is_duration("C1;1;1:4-8;C2"))

    def test_generate_duration(self):
        self.assertEqual(
            generate_duration("TS=200"),
            {"type": "duration", "value": 200}
        )


if __name__ == '__main__':
    unittest.main()
