"""Core Dual-Process Memory Governor implementation."""
from typing import Dict, Any, Callable, Optional


class DualProcessMemoryGovernor:
    def __init__(self, confidence_threshold: float = 0.75):
        self.confidence_threshold = confidence_threshold
        self.system1_cache: Dict[str, Any] = {}
        self.system2_handler: Optional[Callable[[str], Any]] = None
        self.stats = {"system1_hits": 0, "system2_routes": 0}

    def register_system2_handler(self, handler: Callable[[str], Any]):
        self.system2_handler = handler

    def prime_system1(self, query: str, result: Any):
        self.system1_cache[query.strip().lower()] = result

    def estimate_familiarity(self, query: str) -> float:
        norm = query.strip().lower()
        if norm in self.system1_cache:
            return 1.0
        # Partial token match heuristic
        tokens = set(norm.split())
        best = 0.0
        for cached in self.system1_cache:
            c_tokens = set(cached.split())
            if c_tokens:
                overlap = len(tokens.intersection(c_tokens)) / float(len(c_tokens))
                best = max(best, overlap)
        return best

    def retrieve(self, query: str) -> Dict[str, Any]:
        norm = query.strip().lower()
        familiarity = self.estimate_familiarity(norm)

        if familiarity >= self.confidence_threshold and norm in self.system1_cache:
            self.stats["system1_hits"] += 1
            return {
                "route": "System1_Intuitive",
                "result": self.system1_cache[norm],
                "confidence": familiarity,
                "latency_estimate_ms": 1.2
            }

        self.stats["system2_routes"] += 1
        if self.system2_handler:
            result = self.system2_handler(query)
            # Auto-prime System 1 for next time
            self.prime_system1(norm, result)
            return {
                "route": "System2_Deliberative",
                "result": result,
                "confidence": familiarity,
                "latency_estimate_ms": 42.0
            }
        return {
            "route": "Unresolved",
            "result": None,
            "confidence": familiarity,
            "latency_estimate_ms": 0.0
        }
