from dataclasses import dataclass
from typing import List, Dict

from db import DB


@dataclass
class File:
    path: str
    content: str

    def __str__(self):
        return f"{self.path}\n```{self.content}```"


class Project:
    def __init__(self, db: DB):
        self.db = db
        self.staging: Dict[str, File] = {}

    def run(self) -> None:
        pass

    def read_file(self, path) -> File:
        pass

    def read_files(self, paths: List[str]) -> List[File]:
        pass

    def read_all_files(self) -> List[File]:
        return [File(path, content) for path, content in self.db.list()]

    def write_file(self, file: File) -> None:
        self.db[file.path] = file.content

    def write_files(self, files: List[File]) -> None:
        for file in files:
            self.write_file(file)

    def add_file(self, file: File) -> None:
        self.staging[file.path] = file

    def add_files(self, files: List[File]) -> None:
        for file in files:
            self.add_file(file)

    def commit(self) -> None:
        for file in self.staging.values():
            self.write_file(file)
        self.staging = {}

    def is_empty(self) -> bool:
        return self.db.is_empty()

    @property
    def test_entrypoint(self) -> str:
        # static for now
        return "run_tests.sh"

    @property
    def root(self) -> str:
        return self.db.path

    def entrypoint(self) -> File:
        pass

    def deploy(self) -> bool:
        pass
