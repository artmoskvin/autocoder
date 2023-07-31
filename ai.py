from langchain.chat_models.base import BaseChatModel


class AI:
    def __init__(self, model: BaseChatModel):
        self.model = model

    def call(self, prompt: str) -> str:
        return self.model.predict(prompt)
