import random
from typing import Annotated

import typer
from langchain.chat_models import ChatOpenAI
from rich.prompt import Prompt

from agent import CodingAgent
from ai import AI
from chat import format_message, format_prompt
from db import DB
from project import Project

OPENAI_API_KEY = ""

PROMPTS = [
    "What's on the horizon?",
    "What's the next chapter?",
    "Onward and upward! What's next?",
    "What's cooking?",
    "Where do we go from here?",
    "What's our next adventure?",
    "Next stop on our journey?",
    "What's up our sleeve now?",
    "What's the next move on our chessboard?",
    "Rolling forward, what's up next?"
]


def main(project_path: str, model: Annotated[str, typer.Option(help="AI model")] = "gpt-4"):
    db = DB(project_path)
    project = Project(db)
    ai_model = ChatOpenAI(model_name=model, openai_api_key=OPENAI_API_KEY)
    ai = AI(ai_model)
    agent = CodingAgent(ai, project)

    prompt = random.choice(PROMPTS)
    task = Prompt.ask(format_prompt(prompt=prompt))

    agent.run(task)


if __name__ == "__main__":
    typer.run(main)
