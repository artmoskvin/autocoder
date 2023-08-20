from autocoder.agent.code import CodeGenerator
from autocoder.agent.plan import Planner
from autocoder.chat import print_autocoder_msg
from autocoder.project.model import TestRunResult, TestRunSuccess, TestRunFailure
from autocoder.project.project import Project
from autocoder.prompts.testing import fix_it_prompt


class Orchestrator:
    def __init__(self, planner: Planner, code_generator: CodeGenerator, project: Project):
        self.planner = planner
        self.code_generator = code_generator
        self.project = project

    def run(self, task: str) -> None:
        tests_passed = False

        while not tests_passed:
            plan = self.planner.run(task)
            if not plan:
                print_autocoder_msg("Could not create a plan :person_facepalming:")
                return

            self.code_generator.run(plan)

            result: TestRunResult = self.project.run_tests()

            match result:
                case TestRunSuccess():
                    tests_passed = True
                case TestRunFailure(stdout, stderr):
                    task = fix_it_prompt.format(stdout=stdout, stderr=stderr)

        print_autocoder_msg("Work complete :party_popper:")
