"""CLI for dual-process-memory-governor."""
import sys
import argparse
from .governor import DualProcessMemoryGovernor


def main():
    parser = argparse.ArgumentParser(description="Dual-Process Memory Governor CLI")
    parser.add_argument("--demo", action="store_true", help="Run dual-process cognitive routing demo")
    args = parser.parse_args()

    if args.demo:
        gov = DualProcessMemoryGovernor(confidence_threshold=0.8)
        gov.prime_system1("who is current user", {"user": "alice", "role": "admin"})
        gov.register_system2_handler(lambda q: f"Deliberative deep search result for '{q}'")

        res1 = gov.retrieve("who is current user")
        print(f"[+] Route 1: {res1['route']} -> {res1['result']}")

        res2 = gov.retrieve("analyze distributed deadlock in transaction cluster")
        print(f"[+] Route 2: {res2['route']} -> {res2['result']}")
        print(f"[+] Governor Telemetry: {gov.stats}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
