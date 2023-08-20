import os

from autocoder.db import DB
from autocoder.project.model import ProjectType
from autocoder.project.project import Project
from autocoder.project.python_project import PythonProject
from autocoder.project.utils import run_command


class ProjectFactory:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def create(self, project_type: ProjectType, name: str) -> Project:
        match project_type:
            case ProjectType.python:
                return self.__create_python_project(name)
            case _:
                raise NotImplementedError(f"Project type {project_type} is not supported")

    def __create_python_project(self, name: str) -> Project:
        """
        1. create new poetry project
        2. create new DB for the new dir
        3. create new Project with db
        """
        os.makedirs(self.base_dir, exist_ok=True)
        os.chdir(self.base_dir)
        run_command(["poetry", "new", name])

        db = DB(self.base_dir + "/" + name)
        project = PythonProject(db=db, source_code_path=name.replace("-", "_"), tests_path="tests")

        project.add_dependency("pytest")

        return project
