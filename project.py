from dataclasses import dataclass
from typing import List

from db import DB


@dataclass
class File:
    path: str
    content: str


class Project:
    def __init__(self, db: DB):
        self.db = db

    def run(self) -> None:
        pass

    def run_tests(self) -> None:
        pass

    def read_file(self, path) -> File:
        pass

    def read_files(self, paths: List[str]) -> List[File]:
        pass

    def write_file(self, file: File) -> bool:
        pass

    def write_files(self, files: List[File]) -> bool:
        pass

    def test_entrypoint(self) -> File:
        pass

    def entrypoint(self) -> File:
        pass

    def deploy(self) -> bool:
        pass
