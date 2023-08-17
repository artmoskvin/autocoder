import os
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict

from autocoder.db import DB


@dataclass
class File:
    path: str
    content: str

    def __str__(self):
        return f"{self.path}\n```{self.content}```"


class ProjectType(str, Enum):
    python = "python"


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


class ProjectFactory:
    PROJECT_BASE_DIR = "/Users/artemm/Code/autocoder-projects"

    @classmethod
    def create(cls, project_type: ProjectType, name: str) -> Project:
        match project_type:
            case ProjectType.python:
                return cls.__create_python_project(name)
            case _:
                raise NotImplementedError(f"Project type {project_type} is not supported")

    @classmethod
    def __create_python_project(cls, name: str) -> Project:
        """
        1. if not python, exit
        2. create new poetry project
        3. create new DB for the new dir
        4. create new Project with db
        """
        os.makedirs(cls.PROJECT_BASE_DIR, exist_ok=True)
        # os.chdir(cls.PROJECT_BASE_DIR)
        process = subprocess.run(["poetry", "new", name], capture_output=True, text=True)

        if process.returncode:
            stdout_logs = f"Test run stdout:\n{process.stdout}"
            stderr_logs = f"Test run stderr:\n{process.stderr}"
            returncode_logs = f"Test run returncode: {process.returncode}"

        logger.info(stdout_logs)
        logger.info(stderr_logs)
        logger.info(returncode_logs)
        pass
