import unittest

from ..service import is_service, generate_service


class TestService(unittest.TestCase):
    def test_is_service(self):
        self.assertTrue(is_service("C1;1;1:4-8;C2"))
        self.assertTrue(is_service("C2;2;1:4-8,2:5-8;C2"))
        self.assertTrue(is_service("C3;1;1:4-8;S1"))
        self.assertFalse(is_service("TS=123"))
        self.assertFalse(is_service("S1"))
        self.assertFalse(is_service("G1"))

    def test_generate_service(self):
        self.assertEqual(
            generate_service("C1;1;1:4-8;C2"),
            {
                "type": "service",
                "id": 1,
                "attendants": [
                    {"id": 1, "min": 4, "max": 8}
                ],
                "next": {
                    "type": "service",
                    "id": 2
                },
            }
        )


if __name__ == '__main__':
    unittest.main()
