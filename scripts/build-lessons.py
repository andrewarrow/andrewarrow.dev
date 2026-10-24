#!/usr/bin/env python3
"""Build static lesson pages from shared templates and per-lesson HTML."""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
LESSON_PATTERN = "lesson-[0-9][0-9][0-9][0-9][0-9]"
HEADER_PATH = ROOT / "templates" / "lessons" / "header.html"
FOOTER_PATH = ROOT / "templates" / "lessons" / "footer.html"


def read_source(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise RuntimeError(f"cannot read {path.relative_to(ROOT)}: {error.strerror}") from None


def render_pages() -> list[tuple[Path, bytes]]:
    header = read_source(HEADER_PATH)
    footer = read_source(FOOTER_PATH)
    lessons = sorted(path for path in ROOT.glob(LESSON_PATTERN) if path.is_dir())
    if not lessons:
        raise RuntimeError(f"no lesson folders matching {LESSON_PATTERN} found")

    rendered = []
    for lesson in lessons:
        source_path = lesson / "content.html"
        content = read_source(source_path)
        rendered.append((lesson / "index.html", header + content + footer))
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report missing or outdated generated pages without writing files",
    )
    args = parser.parse_args()

    try:
        pages = render_pages()
        if args.check:
            stale = []
            for output, expected in pages:
                try:
                    actual = output.read_bytes()
                except FileNotFoundError:
                    stale.append(f"missing: {output.relative_to(ROOT)}")
                    continue
                except OSError as error:
                    raise RuntimeError(f"cannot read {output.relative_to(ROOT)}: {error.strerror}") from None
                if actual != expected:
                    stale.append(f"out of date: {output.relative_to(ROOT)}")
            if stale:
                print("Lesson pages need a rebuild:")
                for item in stale:
                    print(f"  {item}")
                print("Run: python3 scripts/build-lessons.py")
                return 1
            print(f"All {len(pages)} lesson pages are up to date.")
            return 0

        updated = []
        current = 0
        for output, expected in pages:
            try:
                actual = output.read_bytes()
            except FileNotFoundError:
                actual = None
            except OSError as error:
                raise RuntimeError(f"cannot read {output.relative_to(ROOT)}: {error.strerror}") from None
            if actual == expected:
                current += 1
                continue
            try:
                output.write_bytes(expected)
            except OSError as error:
                raise RuntimeError(f"cannot write {output.relative_to(ROOT)}: {error.strerror}") from None
            updated.append(output.relative_to(ROOT).as_posix())

        if updated:
            print(f"Built {len(updated)} lesson page(s):")
            for path in updated:
                print(f"  {path}")
        else:
            print(f"All {current} lesson pages already current.")
        return 0
    except RuntimeError as error:
        print(f"build-lessons: error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
