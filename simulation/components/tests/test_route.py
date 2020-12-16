import unittest

from ..route import is_route, generate_route


class TestRoute(unittest.TestCase):
    def test_is_route(self):
        self.assertTrue(is_route("R1;0.3-C2;0.7-S1"))
        self.assertTrue(is_route("R1;0.3-C1;0.4-S1;0.3-S2"))
        self.assertFalse(is_route("TS=123"))
        self.assertFalse(is_route("C1;1;1:4-8;C2"))

    def test_generate_route(self):
        self.assertEqual(
            generate_route("R1;0.3-C2;0.7-S1"),
            {
                "type": "route",
                "id": 1,
                "routes": [
                    {"percentage": 0.3, "next": {"type": "service", "id": 2}},
                    {"percentage": 0.7, "next": {"type": "exit", "id": 1}}
                ],
            }
        )


if __name__ == '__main__':
    unittest.main()
