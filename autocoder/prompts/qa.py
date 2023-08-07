from langchain import PromptTemplate

FIX_IT_TEMPLATE = """\
Test run failed with:

{test_run_details}

Fix it.
"""

fix_it_prompt = PromptTemplate.from_template(FIX_IT_TEMPLATE)
