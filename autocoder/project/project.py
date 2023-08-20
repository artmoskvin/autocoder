import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict

from autocoder.db import DB
from autocoder.project.model import File, TestRunResult, TestRunFailure, TestRunSuccess
from autocoder.project.utils import run_command, CommandResult

logger = logging.getLogger(__name__)


class Project(ABC):
    def __init__(self, db: DB, source_code_path: str, tests_path: str):
        self.db = db
        self.root = self.db.path
        self.source_code_path = source_code_path
        self.tests_path = tests_path
        self.staging: Dict[Path, File] = {}

    @property
    @abstractmethod
    def run_tests_command(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def add_dependency_command(self) -> List[str]:
        pass

    @abstractmethod
    def is_system_file(self, file: Path) -> bool:
        pass

    def run_tests(self) -> TestRunResult:
        os.chdir(self.root)
        result: CommandResult = run_command(self.run_tests_command)

        if result.returncode == 5:
            logger.warning("No tests were collected")
            return TestRunSuccess()

        if result.returncode:
            return TestRunFailure(result.stdout, result.stderr)

        return TestRunSuccess()

    def add_dependency(self, dependency) -> CommandResult:
        os.chdir(self.root)
        return run_command(self.add_dependency_command + [dependency])

    def read_all_files(self, include_system: bool = False) -> List[File]:
        return self.db.list() if include_system else self.db.list(ignore=self.is_system_file)

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
