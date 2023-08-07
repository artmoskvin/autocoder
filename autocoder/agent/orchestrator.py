import ast
from typing import List

import typer
from langchain.schema import SystemMessage, HumanMessage, AIMessage, BaseMessage

from autocoder.agent.code import CodeGenerator
from autocoder.agent.qa import QA, Success, Failure
from autocoder.ai import AI
from autocoder.chat import print_msg, ask_approval, prompt
from autocoder.project import Project
from autocoder.prompts.planning import PLAN_PROMPT, QUESTIONS_PROMPT
from autocoder.prompts.qa import fix_it_prompt
from autocoder.prompts.system import SYSTEM_PROMPT, project_prompt


class Orchestrator:
    def __init__(self, ai: AI, project: Project, chat: List[BaseMessage], code_generator: CodeGenerator, qa: QA):
        self.ai = ai
        self.project = project
        self.chat = chat
        self.code_generator = code_generator
        self.qa = qa

    def run(self, task: str) -> None:
        qa_passed = False

        while not qa_passed:
            messages = self.init_messages(task)
            self.chat.extend(messages)
            plan = self.generate_plan()
            if not plan:
                print_msg("Could not create a plan :person_facepalming:")
                raise typer.Abort()

            self.code_generator.run(plan)

            result = self.qa.run_tests()

            match result:
                case Success():
                    qa_passed = True
                case Failure(details):
                    task = fix_it_prompt.format(test_run_details=details)

        print_msg("Work complete :party_popper:")

    def init_messages(self, task):
        if self.project.is_empty():
            messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=task)]
        else:
            files = self.project.read_all_files()
            files_str = "\n".join(str(file) for file in files)
            messages = [SystemMessage(content=SYSTEM_PROMPT),
                        SystemMessage(content=project_prompt.format(files=files_str)),
                        HumanMessage(content=task)]
        return messages

    def generate_plan(self) -> str:
        plan = None
        approved = False
        while not approved:
            questions = self.generate_questions()
            if questions:
                print_msg("Before we proceed there are a few things I need to clarify")
                self.ask_questions(questions)

            plan = self.generate_plan_from_chat()

            plan_msg = f"Here's what I propose\n\n{plan}"
            self.chat.append(AIMessage(content=plan_msg))
            print_msg(plan_msg)

            ask_approval_msg = "Do you approve this plan?"
            self.chat.append(AIMessage(content=ask_approval_msg))
            approved = ask_approval(ask_approval_msg)

            if not approved:
                ask_feedback_msg = "What would you like to add?"
                self.chat.extend([AIMessage(content=ask_feedback_msg),
                                  HumanMessage(content=prompt(ask_feedback_msg))])

        return plan

    def generate_questions(self) -> List[str]:
        self.chat.append(SystemMessage(content=QUESTIONS_PROMPT))
        print_msg("Thinking... :thinking_face:")
        questions_str = self.ai.call(self.chat)
        return ast.literal_eval(questions_str)

    def generate_plan_from_chat(self) -> str:
        self.chat.append(SystemMessage(content=PLAN_PROMPT))
        print_msg("Thinking... :thinking_face:")
        return self.ai.call(self.chat)

    def ask_questions(self, questions: List[str]) -> None:
        while questions:
            q = questions.pop(0)
            self.chat.append(AIMessage(content=q))
            answer = prompt(q)
            self.chat.append(HumanMessage(content=answer))
