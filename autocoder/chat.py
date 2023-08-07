import rich
from rich.prompt import Prompt, Confirm
from rich.text import Text

AUTOCODER_HANDLE = "[bold red]Autocoder[/bold red]"
USER_HANDLE = "[bold green]You[/bold green]"


def format_message(message: str) -> str:
    return f"{AUTOCODER_HANDLE}: {message}"


def format_prompt(prompt: str) -> str:
    return f"{AUTOCODER_HANDLE}: {prompt}\n{USER_HANDLE}"


class ChatLikeConfirm(Confirm):
    prompt_suffix = Text.from_markup(f"\n{USER_HANDLE}: ")


def print_msg(message: str) -> None:
    rich.print(format_message(message))


def ask_approval(message: str) -> str:
    return ChatLikeConfirm.ask(format_message(message))


def prompt(message: str) -> str:
    return Prompt.ask(format_prompt(message))
