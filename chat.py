from rich.prompt import Prompt
from rich.text import Text

AUTOCODER_HANDLE = "[bold red]Autocoder[/bold red]"
USER_HANDLE = "[bold green]You[/bold green]"


def format_message(message: str) -> str:
    return f"{AUTOCODER_HANDLE}: {message}"


def format_prompt(prompt: str) -> str:
    return f"{AUTOCODER_HANDLE}: {prompt}\n{USER_HANDLE}"


class ChatLikePrompt(Prompt):
    prompt_suffix = Text.from_markup(f"\n{USER_HANDLE}: ")
