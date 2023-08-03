import ast
from dataclasses import dataclass
from typing import List

import typer
from langchain.schema import SystemMessage, HumanMessage, AIMessage, BaseMessage

from ai import AI
from chat import print_msg, ask_approval, prompt
from parser import to_files
from project import Project, File
from prompts.coding import CODING_TASK_PROMPT
from prompts.planning import SYSTEM_PROMPT, PLAN_PROMPT, QUESTIONS_PROMPT


@dataclass
class Message:
    user: str
    message: str

    def __str__(self):
        return f"{self.user}: '{self.message}'"


class CodingAgent:
    def __init__(self, ai: AI, project: Project, chat: List[BaseMessage]):
        self.ai = ai
        self.project = project
        self.chat = chat

    def run(self, task: str):
        self.chat.extend([SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=task)])
        plan = self.generate_plan()
        if not plan:
            print_msg("Could not create a plan :person_facepalming:")
            raise typer.Abort()

        files = self.generate_code(plan)
        if not files:
            print_msg("Could not write code :person_facepalming:")
            raise typer.Abort()

        self.project.write_files(files)

        print_msg("Code created :party_popper:")
        raise typer.Exit()

    def generate_plan(self) -> str:
        print_msg("Drafting a plan... :writing_hand:")
        plan = None
        approved = False
        while not approved:
            questions = self.generate_questions()
            if questions:
                print_msg("Before we proceed there are a few things I need to clarify")
                self.ask_questions(questions)

            print_msg("Thank you for answering :folded_hands:")
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

    def generate_code(self, plan: str) -> List[File]:
        approved = False
        files = None
        messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=f"Plan: {plan}"),
                    HumanMessage(content=CODING_TASK_PROMPT)]
        while not approved:
            code_str = self.ai.call(messages)
            files = to_files(code_str)
            self.project.add_files(files)
            files_str = "\n\n".join(list(str(file) for file in files))

            proposal = f"Here's what I propose.\n\n{files_str}\n\n"
            messages.append(AIMessage(content=proposal))
            print_msg(proposal)

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
