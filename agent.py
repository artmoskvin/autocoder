import ast
from dataclasses import dataclass
from typing import List

import rich
import typer
from rich.prompt import Prompt

from ai import AI
from chat import format_message, format_prompt, ChatLikePrompt
from project import Project
from prompts.planning import questions_prompt, plan_prompt


@dataclass
class Message:
    user: str
    message: str

    def __str__(self):
        return f"{self.user}: '{self.message}'"


class CodingAgent:
    def __init__(self, ai: AI, project: Project):
        self.ai = ai
        self.project = project

    def run(self, task: str):
        plan = self.generate_plan(task)
        if not plan:
            rich.print(format_message("Could not create a plan :person_facepalming:"))
            raise typer.Abort()

        rich.print(format_message("Plan created :party_popper:"))
        raise typer.Exit()

        # files = self.generate_code(plan)
        # self.project.write_files(files)
        # self.update_tests()

    def generate_plan(self, task: str) -> str:
        rich.print(format_message("Drafting a plan... :writing_hand:"))
        plan = None
        approved = False
        chat = [Message(user="Client", message=task)]
        while not approved:
            questions = self.generate_questions(chat)
            if questions:
                rich.print(format_message("Before we proceed there are a few things I need to clarify"))
                qa_history = self.ask_questions(questions)
                chat.extend(qa_history)

            rich.print(format_message("Thank you for answering :folded_hands:"))
            plan = self.generate_plan_from_chat(chat)
            rich.print(format_message("Here's what I propose"))
            rich.print(format_message(plan))
            approved = ChatLikePrompt.ask(format_message("Do you approve this plan?"))
            if not approved:
                chat.append(Prompt.ask(format_prompt("What would you like to add?")))

        return plan

    def generate_questions(self, chat: List[Message]) -> List[str]:
        prompt = questions_prompt.format(chat_history="\n".join([str(message) for message in chat]))
        questions_str = self.ai.call(prompt)
        return ast.literal_eval(questions_str)

    def generate_plan_from_chat(self, chat: List[Message]) -> str:
        prompt = plan_prompt.format(chat_history="\n".join([str(message) for message in chat]))
        rich.print(format_message("Thinking... :thinking_face:"))
        return self.ai.call(prompt)

    def ask_questions(self, questions: List[str]) -> List[Message]:
        chat_history: List[Message] = []
        while questions:
            q = questions.pop(0)
            chat_history.append(Message(user="You", message=q))
            answer = Prompt.ask(format_prompt(q))
            chat_history.append(Message(user="Client", message=answer))
        return chat_history
