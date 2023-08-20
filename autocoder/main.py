import logging
import os
import random
from typing import Annotated, Optional

import typer
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from rich.prompt import Prompt
from wonderwords import RandomWord

from autocoder.agent.code import CodeGenerator
from autocoder.agent.orchestrator import Orchestrator
from autocoder.agent.plan import Planner
from autocoder.ai import AI
from autocoder.chat import format_prompt
from autocoder.db import DB
from autocoder.project.factory import ProjectFactory
from autocoder.project.model import ProjectType

logging.basicConfig(level=logging.INFO)

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

MODEL = "gpt-4"

TEMPERATURE = 0

DEFAULT_PATH = "."

PROJECT_BASE_DIR = "/Users/artemm/Code/autocoder-projects"

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

w = RandomWord()

project_factory = ProjectFactory(PROJECT_BASE_DIR)


@app.command()
def new(project_type: Annotated[ProjectType, typer.Argument()], name: Annotated[Optional[str], typer.Option()] = None,
        model: Annotated[str, typer.Option(help="AI model")] = MODEL):
    name = name or w.word(include_categories=["noun"])
    project = project_factory.create(project_type, name)
    ai_model = ChatOpenAI(model_name=model, openai_api_key=OPENAI_API_KEY, temperature=TEMPERATURE)
    ai = AI(ai_model)
    planner = Planner(ai, project)
    code_generator = CodeGenerator(ai, project)
    orchestrator = Orchestrator(planner, code_generator, project)

    while True:
        prompt = random.choice(PROMPTS)
        task = Prompt.ask(format_prompt(prompt=prompt))

        orchestrator.run(task)


@app.command()
def main(project_path: Annotated[str, typer.Argument()] = DEFAULT_PATH,
         model: Annotated[str, typer.Option(help="AI model")] = MODEL):
    pass
    # db = DB(project_path)
    # project = Project(db)
    # ai_model = ChatOpenAI(model_name=model, openai_api_key=OPENAI_API_KEY, temperature=TEMPERATURE)
    # ai = AI(ai_model)
    # planner = Planner(ai, project)
    # code_generator = CodeGenerator(ai, project)
    # qa = QA(project)
    # orchestrator = Orchestrator(planner, code_generator, qa)
    #
    # while True:
    #     prompt = random.choice(PROMPTS)
    #     task = Prompt.ask(format_prompt(prompt=prompt))
    #
    #     orchestrator.run(task)
