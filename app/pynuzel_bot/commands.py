import asyncio
import json
import logging
from typing import Optional

from signalbot import Command, Context

from pynuzel_bot.airtable import (
    Message,
    get_help_message,
    get_latest_intel,
    get_random_joke_by_subjects,
)

CMD_IDENTIFIER: str = "/"


def create_payload(message: Optional[Message], command_identifier: str) -> str:
    return (
        message.text
        if message
        else f"Connection lost with HQ. No {command_identifier} available at the moment."
    )


class HelpCommand(Command):
    def __init__(self, recipients: Optional[list[str]] = None) -> None:
        super().__init__()
        self.recipients = recipients
        self.str_identifier: str = "help"

    async def handle(self, context: Context) -> None:
        command: str = context.message.text

        if not command.lower().strip() == f"{CMD_IDENTIFIER}{self.str_identifier}":
            return

        help = get_help_message()
        payload = create_payload(help, self.str_identifier)

        if not self.recipients:
            recipients = [context.message.group]
        else:
            recipients = self.recipients

        await asyncio.gather(
            *[context.bot.send(recipient, payload) for recipient in recipients]
        )


class IntelCommand(Command):
    def __init__(self, recipients: Optional[list[str]] = None) -> None:
        super().__init__()
        self.recipients = recipients
        self.str_identifier: str = "intel"

    async def handle(self, context: Context) -> None:
        command: str = context.message.text

        if not command.lower().strip() == f"{CMD_IDENTIFIER}{self.str_identifier}":
            return

        intel = get_latest_intel()
        payload = create_payload(intel, self.str_identifier)

        if not self.recipients:
            recipients = [context.message.group]
        else:
            recipients = self.recipients

        await asyncio.gather(
            *[context.bot.send(recipient, payload) for recipient in recipients]
        )


class JokeCommand(Command):
    def __init__(self, recipients: Optional[list[str]] = None) -> None:
        super().__init__()
        self.recipients = recipients
        self.str_identifier: str = "joke"

    async def handle(self, context: Context) -> None:
        command: str = context.message.text

        if not command.lower().strip() == f"{CMD_IDENTIFIER}{self.str_identifier}":
            return

        raw_message = json.loads(context.message.raw_message)
        sender_first_name = raw_message["envelope"].get("sourceName").split(" ")[0]
        logging.warning(sender_first_name)

        joke = get_random_joke_by_subjects(["General", sender_first_name])
        payload = create_payload(joke, self.str_identifier)

        if not self.recipients:
            recipients = [context.message.group]
        else:
            recipients = self.recipients

        await asyncio.gather(
            *[context.bot.send(recipient, payload) for recipient in recipients]
        )


class ForwardCommand(Command):
    def __init__(self, recipients: Optional[list[str]] = None) -> None:
        super().__init__()
        self.recipients = recipients
        self.str_identifier: str = "forward"

    async def handle(self, context: Context) -> None:
        command: str = context.message.text
        identifier = f"{CMD_IDENTIFIER}{self.str_identifier}"

        if not command.lower().startswith(identifier):
            return

        payload = command.split(identifier, 1)[1].strip()

        if not self.recipients:
            recipients = [context.message.group]
        else:
            recipients = self.recipients

        await asyncio.gather(
            *[context.bot.send(recipient, payload) for recipient in recipients]
        )
