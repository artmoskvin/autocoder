from langchain import PromptTemplate

QUESTIONS_TEMPLATE = """\
You are an experienced full-stack software engineer. You received a task from a client. \
Your first step is to create a plan for the implementation of this task. 

Chat history with the client:
{chat_history}

Do you have any questions for how to implement the task? Don't ask about deadlines. Don't ask about budget. \
Return these questions as a Python list. If you have no questions, return an empty list.
"""

questions_prompt = PromptTemplate.from_template(QUESTIONS_TEMPLATE)

PLAN_TEMPLATE = """\
You are an experienced full-stack software engineer. You received a task from a client. \
Your first step is to create a plan for the implementation of this task. 

Chat history with the client:
{chat_history}

Based on the chat history above provide a high-level summary of your plan and list all the files you want to create \
with short description. Don't use the word 'client' in the plan.
"""

plan_prompt = PromptTemplate.from_template(PLAN_TEMPLATE)
