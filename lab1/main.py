from __future__ import annotations

import argparse
import sys
from pathlib import Path
import random

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.application import SessionService
from src.interfaces import run_cli


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diploma defense CLI simulator")
    parser.add_argument("--slot", type=int, default=1, help="Save slot number (>= 1)")
    parser.add_argument(
        "--new",
        action="store_true",
        help="Start a new session in selected slot",
    )
    parser.add_argument("--seed", type=int, default=random.randint(-10000, 10000), help="Optional random seed")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    saves_dir = Path(__file__).resolve().parent / "saves"
    service = SessionService(saves_dir=saves_dir)
    run_cli(service=service, slot=args.slot, create_new=args.new, seed=args.seed)


if __name__ == "__main__":
    main()
