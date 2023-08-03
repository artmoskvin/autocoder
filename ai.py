import logging
from typing import List

from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseMessage

logger = logging.getLogger(__name__)


class AI:
    def __init__(self, model: BaseChatModel):
        self.model = model

    def call(self, messages: List[BaseMessage]) -> str:
        logger.info(f"Calling AI with prompt:\n{messages}")
        return self.model(messages).content
