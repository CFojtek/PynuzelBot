import os
from typing import Optional

from signalbot import Command, Context

from pynuzel_bot.airtable import (
    Message,
    get_help_message,
    get_latest_intel,
    get_random_joke,
)

CMD_IDENTIFIER: str = "/"


def create_payload(message: Optional[Message], command_identifier: str) -> str:
    return (
        message.text
        if message
        else f"Connection lost with HQ. No {command_identifier} available at the moment."
    )


class HelpCommand(Command):
    def setup(self):
        self.str_identifier: str = "help"

    async def handle(self, context: Context) -> None:
        command: str = context.message.text

        if not command.lower().strip() == f"{CMD_IDENTIFIER}{self.str_identifier}":
            return

        help = get_help_message()
        recipient = os.environ["USER_GROUP"]
        payload = create_payload(help, self.str_identifier)

        await context.bot.send(recipient, payload)


class IntelCommand(Command):
    def setup(self):
        self.str_identifier: str = "intel"

    async def handle(self, context: Context) -> None:
        command: str = context.message.text

        if not command.lower().strip() == f"{CMD_IDENTIFIER}{self.str_identifier}":
            return

        intel = get_latest_intel()
        recipient = os.environ["USER_GROUP"]
        payload = create_payload(intel, self.str_identifier)

        await context.bot.send(recipient, payload)


class JokeCommand(Command):
    def setup(self):
        self.str_identifier: str = "joke"

    async def handle(self, context: Context) -> None:
        command: str = context.message.text

        if not command.lower().strip() == f"{CMD_IDENTIFIER}{self.str_identifier}":
            return

        joke = get_random_joke()
        recipient = os.environ["USER_GROUP"]
        payload = create_payload(joke, self.str_identifier)

        await context.bot.send(recipient, payload)


command_list: list[type[HelpCommand] | type[IntelCommand] | type[JokeCommand]] = [
    HelpCommand,
    IntelCommand,
    JokeCommand,
]
