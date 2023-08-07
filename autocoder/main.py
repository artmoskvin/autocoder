import logging
import os
import random
from typing import Annotated

import typer
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from rich.prompt import Prompt

from autocoder.agent.code import CodeGenerator
from autocoder.agent.orchestrator import Orchestrator
from autocoder.agent.qa import QA
from autocoder.ai import AI
from autocoder.chat import format_prompt
from autocoder.db import DB
from autocoder.project import Project

logging.basicConfig(level=logging.INFO)

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

MODEL = "gpt-4"

TEMPERATURE = 0

DEFAULT_PATH = "."

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

app = typer.Typer()


@app.command()
def main(project_path: Annotated[str, typer.Argument()] = DEFAULT_PATH,
         model: Annotated[str, typer.Option(help="AI model")] = MODEL):
    db = DB(project_path)
    project = Project(db)
    ai_model = ChatOpenAI(model_name=model, openai_api_key=OPENAI_API_KEY, temperature=TEMPERATURE)
    ai = AI(ai_model)
    code_generator = CodeGenerator(ai, project)
    qa = QA(project)
    orchestrator = Orchestrator(ai, project, [], code_generator, qa)

    while True:
        prompt = random.choice(PROMPTS)
        task = Prompt.ask(format_prompt(prompt=prompt))

        orchestrator.run(task)
