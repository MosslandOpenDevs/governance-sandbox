from __future__ import annotations

import argparse
import json

from .engine import simulate_governance


def main() -> None:
    parser = argparse.ArgumentParser(prog="gov-sandbox")
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run a governance scenario rehearsal")
    run_cmd.add_argument("--proposal", required=True, help="Governance proposal text")
    run_cmd.add_argument(
        "--stakeholders",
        required=True,
        help="Comma-separated stakeholder list",
    )

    args = parser.parse_args()

    if args.command == "run":
        stakeholders = [item.strip() for item in args.stakeholders.split(",") if item.strip()]
        result = simulate_governance(args.proposal, stakeholders)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
