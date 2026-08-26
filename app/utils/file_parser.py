import re


FILE_PATTERN = re.compile(
    r"FILE:\s*(.*?)\s*```[^\n]*\n(.*?)```",
    re.DOTALL
)


def parse_files(text: str) -> dict[str, str]:

    files = {}

    matches = FILE_PATTERN.findall(
        text or ""
    )

    for filename, content in matches:

        files[filename.strip()] = content.strip()

    return files