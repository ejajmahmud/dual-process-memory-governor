"""Unit tests for dual-process-memory-governor."""
import unittest
from dual_process_memory_governor.governor import DualProcessMemoryGovernor


class TestDualProcessMemoryGovernor(unittest.TestCase):
    def setUp(self):
        self.gov = DualProcessMemoryGovernor(confidence_threshold=0.8)
        self.gov.prime_system1("ping", "pong")
        self.gov.register_system2_handler(lambda q: f"deep_{q}")

    def test_system1_route(self):
        res = self.gov.retrieve("ping")
        self.assertEqual(res["route"], "System1_Intuitive")
        self.assertEqual(res["result"], "pong")
        self.assertEqual(self.gov.stats["system1_hits"], 1)

    def test_system2_route_and_auto_prime(self):
        res = self.gov.retrieve("complex_graph_search")
        self.assertEqual(res["route"], "System2_Deliberative")
        self.assertEqual(res["result"], "deep_complex_graph_search")
        # Ensure it was auto-primed into System 1
        res2 = self.gov.retrieve("complex_graph_search")
        self.assertEqual(res2["route"], "System1_Intuitive")
