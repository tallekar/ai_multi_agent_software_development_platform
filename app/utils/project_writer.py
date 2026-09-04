import os
from io import BytesIO
from pathlib import Path, PurePosixPath
from pathlib import PureWindowsPath
from zipfile import ZIP_DEFLATED, ZipFile
from uuid import uuid4


PROJECTS_ROOT = Path(
    os.getenv("GENERATED_PROJECTS_DIR", "generated_projects")
)


def _safe_relative_path(filename: str) -> Path:
    normalized = filename.replace("\\", "/").strip()
    path = PurePosixPath(normalized)
    windows_path = PureWindowsPath(normalized)

    if (
        not normalized
        or path.is_absolute()
        or windows_path.is_absolute()
        or windows_path.drive
        or ".." in path.parts
        or any(not part or part == "." for part in path.parts)
    ):
        raise ValueError(f"Unsafe generated filename: {filename}")

    return Path(*path.parts)


def write_project(files: dict[str, str], root: Path = PROJECTS_ROOT) -> dict:
    project_directory = root / f"project-{uuid4().hex[:12]}"
    project_directory.mkdir(parents=True, exist_ok=False)
    written_files = []

    try:
        for filename, content in files.items():
            relative_path = _safe_relative_path(filename)
            destination = project_directory / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
            written_files.append(relative_path.as_posix())
    except Exception:
        for path in sorted(project_directory.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        project_directory.rmdir()
        raise

    project_path = str(project_directory.resolve())
    return {
        "directory": project_path,
        "project_path": project_path,
        "project_id": project_directory.name,
        "project_name": project_directory.name,
        "files": written_files,
        "generated_files": written_files,
        "file_count": len(written_files),
        "manifest_path": str((project_directory / "project_manifest.json").resolve()),
    }


def update_project(
    project_path: str,
    files: dict[str, str],
    architecture: str = "",
) -> dict:
    project_directory = Path(project_path).resolve()
    if not project_directory.is_dir():
        raise ValueError("Generated project directory not found")

    written_files = []
    for filename, content in files.items():
        relative_path = _safe_relative_path(filename)
        destination = project_directory / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        written_files.append(relative_path.as_posix())

    return {
        "directory": str(project_directory),
        "project_path": str(project_directory),
        "project_id": project_directory.name,
        "project_name": project_directory.name,
        "files": written_files,
        "generated_files": written_files,
        "file_count": len(written_files),
        "manifest_path": str((project_directory / "project_manifest.json").resolve()),
    }


def create_project_zip(project_id: str, root: Path = PROJECTS_ROOT) -> BytesIO:
    project_directory = (root / project_id).resolve()
    projects_root = root.resolve()

    if (
        project_directory.parent != projects_root
        or not project_directory.is_dir()
    ):
        raise FileNotFoundError(project_id)

    archive = BytesIO()

    with ZipFile(archive, "w", ZIP_DEFLATED) as zip_file:
        for file_path in project_directory.rglob("*"):
            if file_path.is_file():
                zip_file.write(
                    file_path,
                    file_path.relative_to(project_directory).as_posix(),
                )

    archive.seek(0)
    return archive