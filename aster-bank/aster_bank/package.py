"""Build the self-contained Python edition of the project."""

from argparse import ArgumentParser
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
PROJECT_FILES = (
    "server.py",
    ".gitignore",
    "aster_bank/__init__.py",
    "aster_bank/bank.py",
    "aster_bank/server.py",
    "aster_bank/package.py",
    "dist/client/index.html",
    "dist/client/styles.css",
    "dist/client/app.mjs",
    "dist/client/aster.svg",
    "dist/client/inter.woff2",
    "dist/client/Inter-OFL.txt",
    "docs/use-case.svg",
    "drizzle/0000_initial.sql",
)


def documentation_path(root: Path, target: str) -> Path:
    """Prefer the Python-specific documents when building from the hosting checkout."""
    python_doc = root / "python_docs" / Path(target).name
    return python_doc if python_doc.is_file() else root / target


def build_source_zip(root: Path = ROOT) -> bytes:
    project = {name: root / name for name in PROJECT_FILES}
    for name in ("README.md", "docs/transfer-sequence.svg", "docs/project-guide.md"):
        project[name] = documentation_path(root, name)
    for test in (root / "tests").glob("test_*.py"):
        project[f"tests/{test.name}"] = test

    output = BytesIO()
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for name, path in sorted(project.items()):
            entry = ZipInfo(f"aster-bank/{name}", (2024, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
    return output.getvalue()


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(build_source_zip())


if __name__ == "__main__":
    main()
