import unittest

from ..components import (
    get_base_component_info,
    get_components_stats,
    get_components_base_stats,
    get_entrance_stats,
    get_service_stats,
    get_services_queues_stats,
    get_route_stats,
    get_exit_stats
)


class TestComponents(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.units_a = [{
            "id": "d40168b9-4e23-43bd-9bd6-9eef92a18b1f",
            "history": [
                {"at": 1, "duration": 0, "type": "entrance", "id": 1},
                {"at": 1, "duration": 19, "type": "service", "id": 1},
                {"at": 20, "duration": 0, "type": "route", "id": 1},
                {"at": 20, "type": "exit", "id": 1}
            ]
        }]

        self.components_stats = {
            "entrances": {},
            "services": {},
            "routes": {},
            "exits": {}
        }

    def test_get_base_component_info(self):
        entrances_a = {"at": 1, "duration": 0, "type": "entrance", "id": 1}
        entrances_b = {"at": 15, "duration": 0, "type": "entrance", "id": 1}

        self.assertEqual(
            get_base_component_info(
                entrances_a,
                self.components_stats["entrances"]
            ),
            {
                "first_entrance": 1,
                "last_entrance": 1,
                "attendances": 1
            }
        )

        self.components_stats["entrances"] = {
            1: get_entrance_stats(entrances_a, self.components_stats)
        }

        self.assertEqual(
            get_base_component_info(
                entrances_b,
                self.components_stats["entrances"]
            ),
            {
                "first_entrance": 1,
                "last_entrance": 15,
                "attendances": 2
            }
        )

    def test_get_components_base_stats(self):
        self.assertEqual(
            get_components_base_stats(self.units_a),
            {
                "entrances": {
                    1: {
                        "first_entrance": 1,
                        "last_entrance": 1,
                        "attendances": 1
                    }
                },
                "services": {
                    1: {
                        "first_entrance": 1,
                        "last_entrance": 1,
                        "attendances": 1,
                        "attending_time": 19
                    }
                },
                "routes": {
                    1: {
                        "first_entrance": 20,
                        "last_entrance": 20,
                        "attendances": 1
                    }
                },
                "exits": {
                    1: {
                        "first_entrance": 20,
                        "last_entrance": 20,
                        "attendances": 1
                    }
                }
            }
        )

    def test_get_components_stats(self):
        components = get_components_stats(self.units_a)
        self.assertEqual(
            components["services"],
            {
                1: {
                    "average_waiting_time": 0,
                    "probability_of_waiting": 0,
                    "biggest_waiting_time": 0,
                    "average_service_duration": 19.0,
                    "attending_time": 19,
                    "first_entrance": 1,
                    "last_entrance": 1,
                    "attendances": 1
                }
            }
        )

    def test_get_entrance_stats(self):
        entrance_a = {"at": 1, "duration": 0, "type": "entrance", "id": 1}
        entrance_b = {"at": 10, "duration": 0, "type": "entrance", "id": 1}

        self.assertEqual(
            get_entrance_stats(entrance_a, self.components_stats),
            get_base_component_info(
                entrance_a, self.components_stats["entrances"])
        )

        self.components_stats["entrances"] = {
            1: get_entrance_stats(entrance_a, self.components_stats)
        }

        self.assertEqual(
            get_entrance_stats(entrance_b, self.components_stats),
            get_base_component_info(
                entrance_b, self.components_stats["entrances"])
        )

    def test_get_service_stats(self):
        service_a = {"at": 1, "duration": 5, "type": "service", "id": 1}
        service_b = {"at": 10, "duration": 8, "type": "service", "id": 1}

        self.assertEqual(
            get_service_stats(
                service_a,
                self.components_stats
            ),
            {
                "first_entrance": 1,
                "last_entrance": 1,
                "attendances": 1,
                "attending_time": 5
            }
        )

        self.components_stats["services"] = {
            1: get_service_stats(service_a, self.components_stats)
        }

        self.assertEqual(
            get_service_stats(
                service_b,
                self.components_stats
            ),
            {
                "first_entrance": 1,
                "last_entrance": 10,
                "attendances": 2,
                "attending_time": 13
            }
        )

    def test_get_services_queues_stats(self):
        units = [
            {"history": [
                {"at": 1, "duration": 10, "type": "service",
                    "action": "queue", "id": 1},
                {"at": 11, "duration": 5, "type": "service", "id": 1}
            ]},
            {"history": [
                {"at": 11, "duration": 8, "type": "service",
                    "action": "queue", "id": 1},
                {"at": 19, "duration": 10, "type": "service", "id": 1}
            ]},
            {"history": [
                {"at": 19, "duration": 15, "type": "service",
                    "action": "queue", "id": 1},
                {"at": 26, "duration": 15, "type": "service", "id": 1}
            ]},
            {"history": [
                {"at": 50, "duration": 15, "type": "service", "id": 1}
            ]}
        ]

        self.assertEqual(
            get_services_queues_stats(units, get_components_base_stats(units)),
            {1: {
                "average_waiting_time": 11.0,
                "probability_of_waiting": 0.75,
                "biggest_waiting_time": 15,
                "average_service_duration": 11.25,
                "attending_time": 45,
                "first_entrance": 11,
                "last_entrance": 50,
                "attendances": 4
            }}
        )

    def test_get_route_stats(self):
        route_a = {"at": 1, "duration": 0, "type": "route", "id": 1}
        route_b = {"at": 15, "duration": 0, "type": "route", "id": 1}

        self.assertEqual(
            get_route_stats(route_a, self.components_stats),
            get_base_component_info(route_a, self.components_stats["routes"])
        )

        self.components_stats["routes"] = {
            1: get_route_stats(route_a, self.components_stats)
        }

        self.assertEqual(
            get_route_stats(route_b, self.components_stats),
            get_base_component_info(route_b, self.components_stats["routes"])
        )

    def test_get_exit_stats(self):
        exit_a = {"at": 1, "type": "exit", "id": 1}
        exit_b = {"at": 15, "type": "exit", "id": 1}

        self.assertEqual(
            get_exit_stats(exit_a, self.components_stats),
            get_base_component_info(exit_a, self.components_stats["exits"])
        )

        self.components_stats["exits"] = {
            1: get_exit_stats(exit_a, self.components_stats)
        }

        self.assertEqual(
            get_exit_stats(exit_b, self.components_stats),
            get_base_component_info(exit_b, self.components_stats["exits"])
        )
