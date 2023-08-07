import logging
import os
import subprocess
from dataclasses import dataclass

from autocoder.project import Project

logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    pass


@dataclass
class Success(TestResult):
    pass


@dataclass
class Failure(TestResult):
    details: str


class QA:
    def __init__(self, project: Project):
        self.project = project

    def run_tests(self) -> TestResult:
        os.chdir(str(self.project.root))
        process = subprocess.run(["bash", self.project.test_entrypoint], capture_output=True, text=True)

        stdout_logs = f"Test run stdout:\n{process.stdout}"
        stderr_logs = f"Test run stderr:\n{process.stderr}"
        returncode_logs = f"Test run returncode: {process.returncode}"

        logger.info(stdout_logs)
        logger.info(stderr_logs)
        logger.info(returncode_logs)

        if process.returncode:
            details = "\n".join([stdout_logs, stderr_logs, returncode_logs])
            return Failure(details)

        return Success()
