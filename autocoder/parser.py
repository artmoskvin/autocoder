import logging
import re
from pathlib import Path
from typing import List

from autocoder.project.model import File

logger = logging.getLogger(__name__)


def to_files(text: str) -> List[File]:
    # Get all ``` blocks and preceding filenames
    regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
    matches = re.finditer(regex, text, re.DOTALL)

    files = []
    for match in matches:
        # Strip the filename of any non-allowed characters and convert / to \
        path = re.sub(r'[<>"|?*]', "", match.group(1))

        # Remove leading and trailing brackets
        path = re.sub(r"^\[(.*)\]$", r"\1", path)

        # Remove leading and trailing backticks
        path = re.sub(r"^`(.*)`$", r"\1", path)

        # Remove trailing ]
        path = re.sub(r"\]$", "", path)

        # Get the code
        code = match.group(2)

        # Ignore empty directories
        if path.endswith("/"):
            logger.warning(f"Invalid filename {path} with content {code}. File ignored.")
            continue

        # Add the file to the list
        files.append(File(path=Path(path), content=code))

    # Return the files
    return files
