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

    def stream(self, messages: List[BaseMessage]) -> Iterator[BaseMessageChunk]:
        print_system_msg(f"Streaming AI response for prompt:\n{pprint_messages(messages)}")
        for chunk in self.model.stream(messages):
            yield chunk
