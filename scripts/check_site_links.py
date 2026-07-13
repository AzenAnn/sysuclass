"""Validate internal links and fragments in the generated MkDocs site."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def configured_base_path() -> str:
    """Read the GitHub Pages subpath from the simple site_url setting."""
    config = ROOT / "mkdocs.yml"
    for line in config.read_text(encoding="utf-8").splitlines():
        if line.startswith("site_url:"):
            value = line.split(":", 1)[1].strip().strip('"\'')
            return unquote(urlsplit(value).path).rstrip("/")
    return ""


BASE_PATH = configured_base_path()


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"] or "")


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def target_for(origin: Path, href_path: str) -> Path:
    decoded = unquote(href_path)
    if not decoded:
        return origin
    if decoded.startswith("/"):
        if BASE_PATH and (decoded == BASE_PATH or decoded.startswith(f"{BASE_PATH}/")):
            decoded = decoded[len(BASE_PATH) :] or "/"
        target = SITE / decoded.lstrip("/")
    else:
        target = origin.parent / decoded
    target = target.resolve()
    if decoded.endswith("/") or target.is_dir():
        target /= "index.html"
    elif not target.suffix:
        target /= "index.html"
    return target


def main() -> int:
    if not SITE.exists():
        print("找不到 site 目录，请先运行 python -m mkdocs build --strict", file=sys.stderr)
        return 1

    pages = {path.resolve(): parse_page(path) for path in SITE.rglob("*.html")}
    errors: list[str] = []

    for origin, page in pages.items():
        for href in page.hrefs:
            parts = urlsplit(href)
            if parts.scheme or parts.netloc or href.startswith("//"):
                continue
            target = target_for(origin, parts.path)
            try:
                display_target = target.relative_to(SITE.resolve()).as_posix()
            except ValueError:
                errors.append(f"{origin.relative_to(SITE)}: 链接越出站点目录：{href}")
                continue
            if not target.exists():
                errors.append(f"{origin.relative_to(SITE)}: 链接不存在：{href} -> {display_target}")
                continue
            if parts.fragment and target.suffix == ".html":
                target_page = pages.get(target.resolve())
                fragment = unquote(parts.fragment)
                if target_page is not None and fragment not in target_page.ids:
                    errors.append(f"{origin.relative_to(SITE)}: 页内标题不存在：{href}")

    if errors:
        print("站内链接检查失败：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"站内链接检查通过：已检查 {len(pages)} 个页面。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
