from autocoder.agent.code import CodeGenerator
from autocoder.agent.plan import Planner
from autocoder.agent.qa import QA, Success, Failure
from autocoder.chat import print_msg
from autocoder.prompts.qa import fix_it_prompt


class Orchestrator:
    def __init__(self, planner: Planner, code_generator: CodeGenerator, qa: QA):
        self.planner = planner
        self.code_generator = code_generator
        self.qa = qa

    def run(self, task: str) -> None:
        qa_passed = False

        while not qa_passed:
            plan = self.planner.run(task)
            if not plan:
                print_msg("Could not create a plan :person_facepalming:")
                return

            self.code_generator.run(plan)

            result = self.qa.run_tests()

            match result:
                case Success():
                    qa_passed = True
                case Failure(details):
                    task = fix_it_prompt.format(test_run_details=details)

        print_msg("Work complete :party_popper:")
