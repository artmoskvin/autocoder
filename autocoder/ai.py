import logging
from typing import List

from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseMessage

from autocoder.chat import print_system_msg

logger = logging.getLogger(__name__)


def pprint_messages(messages: List[BaseMessage]) -> str:
    return "\n".join([f" > {message.type}: {message.content}" for message in messages])


class AI:
    def __init__(self, model: BaseChatModel):
        self.model = model

    def call(self, messages: List[BaseMessage]) -> str:
        print_system_msg(f"Calling AI with prompt:\n{pprint_messages(messages)}")
        return self.model(messages).content
    def stream_call(self, initial_messages: List[BaseMessage]) -> Generator[str, List[BaseMessage], None]:
        print_system_msg(f"Starting streaming AI with initial prompt:\n{pprint_messages(initial_messages)}")
        partial_completion = self.model(initial_messages).content
        yield partial_completion
        while True:
            try:
                new_messages = yield
                if new_messages:
                    print_system_msg(f"Received new messages for streaming AI:\n{pprint_messages(new_messages)}")
                    partial_completion = self.model(new_messages).content
                    yield partial_completion
            except GeneratorExit:
                print_system_msg("Streaming AI call ended.")
                break
