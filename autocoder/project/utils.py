import logging
import subprocess
from dataclasses import dataclass
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


def run_command(command: List[str]) -> CommandResult:
    process = subprocess.run(command, capture_output=True, text=True)
    return CommandResult(process.returncode, process.stdout or "", process.stderr or "")
