from langchain import PromptTemplate

SYSTEM_PROMPT = """\
You are an experienced full-stack software engineer. You write modular and reusable high-quality code. \
You always cover it with tests."""

PROJECT_TEMPLATE = """\
You're currently working on a project that contains the following files:

{files}
"""

project_prompt = PromptTemplate.from_template(PROJECT_TEMPLATE)
