from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ProjectType(str, Enum):
    python = "python"


@dataclass
class File:
    path: Path
    content: str

    def __str__(self):
        return f"{self.path}\n```{self.content}```"


@dataclass
class TestRunResult:
    pass


@dataclass
class TestRunSuccess(TestRunResult):
    pass


@dataclass
class TestRunFailure(TestRunResult):
    stdout: str
    stderr: str
