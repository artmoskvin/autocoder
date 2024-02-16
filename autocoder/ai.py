from typing import Iterator


class AI:
    def __init__(self, model: BaseChatModel):
        self.model = model

    def call(self, messages: List[BaseMessage]) -> str:
        print_system_msg(f"Calling AI with prompt:\n{pprint_messages(messages)}")
        return ''.join(chunk.content for chunk in self.stream(messages))

    def stream(self, messages: List[BaseMessage]) -> Iterator[BaseMessageChunk]:
        print_system_msg(f"Streaming AI with prompt:\n{pprint_messages(messages)}")
        return self.model.stream(messages)