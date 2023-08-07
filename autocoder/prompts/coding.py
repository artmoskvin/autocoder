CODING_TASK_PROMPT = """\
Implement the files listed in the plan. Each file should contain ALL code. Do not "pass" the implementation.
Each file must strictly follow a markdown code block format, where the FILENAME is the lowercase file name including the 
file extension, LANG is the markup code block language for the code's language, and CODE is the code:

FILENAME
```LANG
CODE
```

The code should be fully functional. No placeholders.
"""
