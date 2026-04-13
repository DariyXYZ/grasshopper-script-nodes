from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Path to the skill repo root.")
    parser.add_argument(
        "--target",
        required=True,
        help="Directory that contains discoverable Codex skills, e.g. %USERPROFILE%\\.codex\\skills",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = Path(args.source).resolve()
    target_root = Path(args.target).expanduser().resolve()
    destination = target_root / source.name

    if not (source / "SKILL.md").exists():
        raise SystemExit(f"Missing SKILL.md in {source}")

    target_root.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        shutil.rmtree(destination)

    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    print(f"Installed {source.name} to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
