from pathlib import Path
from typing import List, Tuple


class DB:
    """A simple key-value store, where keys are filenames and values are file contents."""

    def __init__(self, path):
        self.path = Path(path).absolute()

        self.path.mkdir(parents=True, exist_ok=True)

    def __contains__(self, key):
        return (self.path / key).is_file()

    def __getitem__(self, key):
        full_path = self.path / key

        if not full_path.is_file():
            raise KeyError(f"File '{key}' could not be found in '{self.path}'")
        with full_path.open("r", encoding="utf-8") as f:
            return f.read()

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key, val):
        full_path = self.path / key
        full_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(val, str):
            full_path.write_text(val, encoding="utf-8")
        else:
            # If val is neither a string nor bytes, raise an error.
            raise TypeError("val must be either a str or bytes")

    def is_empty(self) -> bool:
        return not any(self.path.iterdir())

    def list(self) -> List[Tuple[str, str]]:
        files = []
        for file in self.path.rglob('*'):
            if file.is_file():
                # Skip directories like "__pycache__"
                if any(part.startswith('__') for part in file.parts):
                    continue

                # Skip directories like ".pytest_cache"
                if any(part.startswith('.') for part in file.parts):
                    continue

                # Skip directories like "venv"
                if any(part == 'venv' for part in file.parts):
                    continue

                files.append((self.__get_relative_path(file), self.__get_file_content(file)))
        return files

    def __get_file_content(self, file: Path):
        return self[self.__get_relative_path(file)]

    def __get_relative_path(self, path: Path):
        return str(path.relative_to(self.path))
