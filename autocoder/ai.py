f
r
o
m
 
t
y
p
i
n
g
 
i
m
p
o
r
t
 
I
t
e
r
a
t
o
r


f
r
o
m
 
l
a
n
g
c
h
a
i
n
.
s
c
h
e
m
a
 
i
m
p
o
r
t
 
B
a
s
e
M
e
s
s
a
g
e
C
h
u
n
k
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
