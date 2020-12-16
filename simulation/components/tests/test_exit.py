import unittest

from ..exit import is_exit, generate_exit


class TestExit(unittest.TestCase):
    def test_is_exit(self):
        self.assertTrue(is_exit("S1"))
        self.assertTrue(is_exit("S2"))
        self.assertFalse(is_exit("TS=123"))
        self.assertFalse(is_exit("C1;1;1:4-8;C2"))

    def test_generate_exit(self):
        self.assertEqual(
            generate_exit("S1"),
            {"type": "exit", "id": 1}
        )


if __name__ == '__main__':
    unittest.main()
