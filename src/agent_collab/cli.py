from __future__ import annotations

import argparse
from pathlib import Path

from agent_collab.validation import ValidationError, validate_repo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-collab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate repository examples")
    validate.add_argument(
        "root",
        nargs="?",
        default=".",
        help="repository root, defaults to current directory",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "validate":
        root = Path(args.root).resolve()
        try:
            checked = validate_repo(root)
        except ValidationError as exc:
            print(f"validation failed: {exc}")
            return 1
        print(f"validated {len(checked)} files")
        for path in checked:
            print(f"- {path.relative_to(root)}")
        return 0

    raise AssertionError(f"unhandled command: {args.command}")
