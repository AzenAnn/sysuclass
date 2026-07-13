"""Check that course resource files are registered in their inventory page."""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
COURSES = ROOT / "docs" / "courses"
RESOURCE_DIR_NAMES = {"notes", "review", "exams", "homework", "other"}
MAX_BYTES = 25 * 1024 * 1024
IGNORED_NAMES = {".gitkeep", "index.md"}


def check_course(course_dir: Path) -> list[str]:
    resources = course_dir / "resources"
    inventory = resources / "index.md"
    if not resources.exists():
        return []
    if not inventory.exists():
        return [f"{course_dir.name}: 缺少 resources/index.md"]

    inventory_text = unquote(inventory.read_text(encoding="utf-8"))
    errors: list[str] = []

    for path in sorted(resources.rglob("*")):
        if not path.is_file() or path.name in IGNORED_NAMES:
            continue
        relative = path.relative_to(resources).as_posix()
        if path.parent.name not in RESOURCE_DIR_NAMES:
            errors.append(f"{relative}: 请放入 notes/review/exams/homework/other 之一")
        if relative not in inventory_text:
            errors.append(f"{relative}: 未在 resources/index.md 登记链接")
        if path.stat().st_size > MAX_BYTES:
            size_mb = path.stat().st_size / 1024 / 1024
            errors.append(f"{relative}: {size_mb:.1f} MB，超过建议上限 25 MB")

    return [f"{course_dir.name}: {message}" for message in errors]


def main() -> int:
    if not COURSES.exists():
        print("找不到 docs/courses 目录", file=sys.stderr)
        return 1

    errors: list[str] = []
    for course_dir in sorted(path for path in COURSES.iterdir() if path.is_dir()):
        errors.extend(check_course(course_dir))

    if errors:
        print("资源检查失败：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("资源检查通过：所有资料均已登记，且未超过 25 MB。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

