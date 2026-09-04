import re


FILE_BLOCK_PATTERN = re.compile(
    r"^[ \t]*FILE:[ \t]*(?P<path>[^\r\n]+)[ \t]*\r?\n"
    r"(?P<content>.*?)"
    r"(?:\r?\n)?^[ \t]*END_FILE[ \t]*$",
    re.MULTILINE | re.DOTALL,
)


def parse_files(text: str) -> dict[str, str]:
    files = {}

    for match in FILE_BLOCK_PATTERN.finditer(text or ""):
        filename = match.group("path").strip()
        if filename:
            files[filename] = match.group("content")

    return files