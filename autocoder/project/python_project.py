from pathlib import Path
from typing import List

from autocoder.project.project import Project


class PythonProject(Project):
    def files_to_ignore(self) -> List[str]:
        pass

    @property
    def run_tests_command(self) -> List[str]:
        return ["poetry", "run", "pytest"]

    @property
    def add_dependency_command(self) -> List[str]:
        return ["poetry", "add"]

    def is_system_file(self, file: Path) -> bool:
        for part in file.parts:
            # todo: does it also exclude __init__.py? do we need them?
            if part.startswith('__'):
                return True

            if part.startswith('.'):
                return True

            if 'venv' in part:
                return True

            if part == "poetry.lock":
                return True

        return False
