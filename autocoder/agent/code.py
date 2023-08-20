from typing import List

from langchain.schema import SystemMessage, HumanMessage, AIMessage, BaseMessage

from autocoder.ai import AI
from autocoder.chat import print_autocoder_msg, ask_approval, prompt
from autocoder.parser import to_files
from autocoder.project.model import File
from autocoder.project.project import Project
from autocoder.prompts.coding import CODING_TASK_PROMPT
from autocoder.prompts.system import project_prompt


class CodeGenerator:
    def __init__(self, ai: AI, project: Project):
        self.ai = ai
        self.project = project

    def run(self, plan: str) -> None:
        files = self.generate_code(plan)
        if not files:
            print_autocoder_msg("Could not write code :person_facepalming:")
            return

        self.project.write_files(files)

    def generate_code(self, plan: str) -> List[File]:
        approved = False
        files = None
        messages = self.init_messages(plan)
        while not approved:
            code_str = self.ai.call(messages)
            files = to_files(code_str)
            self.project.add_files(files)
            files_str = "\n\n".join(list(str(file) for file in files))

            proposal = f"Here's what I propose.\n\n{files_str}\n\n"
            messages.append(AIMessage(content=proposal))
            print_autocoder_msg(proposal)

            approval_msg = "Does that make sense?"
            messages.append(AIMessage(content=approval_msg))
            approved = ask_approval(approval_msg)

            if not approved:
                feedback_msg = "What would you like to add or change?"
                messages.append(AIMessage(content=feedback_msg))
                feedback = prompt(feedback_msg)
                messages.append(HumanMessage(content=feedback))

        self.project.commit()
        return files

    def init_messages(self, plan: str) -> List[BaseMessage]:
        files = self.project.read_all_files()
        files_str = "\n".join(str(file) for file in files)

        source_code_path = self.project.source_code_path
        tests_path = self.project.tests_path

        messages = [SystemMessage(content=project_prompt.format(files=files_str, source_code_path=source_code_path,
                                                                tests_path=tests_path)),
                    HumanMessage(content=f"Plan: {plan}"),
                    HumanMessage(content=CODING_TASK_PROMPT)]

        return messages
