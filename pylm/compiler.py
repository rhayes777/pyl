import os
from abc import ABC
from dataclasses import dataclass
from typing import Optional

from anthropic import AnthropicBedrock

from pylm.module import Module
from pylm.module_updater import ModuleUpdater
from pylm.session import Function


class Conversation(ABC):
    def __init__(self):
        self.messages = []

    def clear(self):
        self.messages = []


class ClaudeConversation(Conversation):
    def __init__(
        self,
        system: str,
        model="anthropic.claude-3-haiku-20240307-v1:0",
        max_tokens=4096,
    ):
        super().__init__()
        self.system = system
        self.client = AnthropicBedrock(
            aws_region=os.environ.get("AWS_DEFAULT_REGION"),
        )
        self.model = model
        self.max_tokens = max_tokens

    def __call__(self, text: str):
        self.messages.append({"role": "user", "content": text})

        message = self.client.messages.create(
            system=self.system,
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
        )
        text = message.content[0].text

        self.messages.append({"role": "assistant", "content": text})
        return text


@dataclass
class CompiledFunction:
    source: Function
    implementation: str


class Compiler:
    def __init__(
        self,
        module: Module,
        conversation: Optional[Conversation] = None,
    ):
        self.module = module
        self.conversation = conversation or ClaudeConversation(
            system="""
I will give you a function signature and a description of that function. 
Return an implemented Python function with the same signature and description.
Give only the Python code in response.

The signature will be defined in signature tags. The response should be given in <python> tags.

For example:

<signature>
def add(a: int, b: int) -> int:
    '''
    Add two integers.
    '''
</signature>
<python>
def function(a, b):
    '''
    Add together two numbers.

    Args:
        a (int or float): The first number to be added.
        b (int or float): The second number to be added.

    Returns:
        int or float: The sum of the two input numbers.
    '''
    return a + b
</python>
            """
        )

    def compiled_functions(self):
        for function in self.module.functions:
            compiled = self._compile(function)
            self.conversation.clear()
            yield compiled

    def _compile(self, function):
        prompt = f""""
{function.name}{function.signature}
{function.docs}
"""
        implementation = extract_code_from_tags(self.conversation(prompt))
        return CompiledFunction(
            source=function,
            implementation=implementation,
        )

    def compiled_module(self):
        return "\n\n".join(f.implementation for f in self.compiled_functions())

    def run(self):
        target_path = self.module.path.with_suffix(".py")
        with open(target_path, "w") as f:
            f.write(self.module.path.read_text())

        updater = ModuleUpdater(target_path)

        for function in self.compiled_functions():
            updater[function.source.name] = function.implementation


def extract_code_from_tags(code: str) -> str:
    """
    Extract the code from between the <python></python> tags.

    Args:
        code (str): The input string containing the code enclosed in tags.

    Returns:
        str: The extracted code without the tags.
    """
    start_tag = "<python>"
    end_tag = "</python>"

    start_index = code.find(start_tag)
    if start_index == -1:
        return ""

    start_index += len(start_tag)
    end_index = code.find(end_tag)
    if end_index == -1:
        return ""

    return code[start_index:end_index]
