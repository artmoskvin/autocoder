import logging
import os
import random
from typing import Annotated

import typer
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from rich.prompt import Prompt

from agent.code import CodeGenerator
from agent.orchestrator import Orchestrator
from ai import AI
from chat import format_prompt
from db import DB
from project import Project

logging.basicConfig(level=logging.INFO)

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

MODEL = "gpt-4"

TEMPERATURE = 0

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


def main(project_path: str, model: Annotated[str, typer.Option(help="AI model")] = MODEL):
    db = DB(project_path)
    project = Project(db)
    ai_model = ChatOpenAI(model_name=model, openai_api_key=OPENAI_API_KEY, temperature=TEMPERATURE)
    ai = AI(ai_model)
    code_generator = CodeGenerator(ai, project)
    orchestrator = Orchestrator(ai, project, [], code_generator)

    while True:
        prompt = random.choice(PROMPTS)
        task = Prompt.ask(format_prompt(prompt=prompt))

        orchestrator.run(task)


if __name__ == "__main__":
    typer.run(main)
