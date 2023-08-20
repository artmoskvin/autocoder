from pathlib import Path
from typing import List, Callable

from autocoder.project.model import File


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

    def list(self, ignore: Callable[[Path], bool] = lambda p: False) -> List[File]:
        files = []
        for file in self.path.rglob('*'):
            if file.is_file() and not ignore(file):
                files.append(File(self.__get_relative_path(file), self.__get_file_content(file)))
        return files

    def __get_file_content(self, file: Path) -> str:
        return self[self.__get_relative_path(file)]

    def __get_relative_path(self, path: Path) -> Path:
        return path.relative_to(self.path)
