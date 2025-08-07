from typing import LiteralString

from signalbot import Command, Context

from pynuzel_bot.airtable import get_latest_intel, get_random_joke

HELP_MESSAGE: LiteralString = """
*Krr Krr* UnuzelHQ reporting in. To guide you through this zombie apocalypse, you can use following commands.

    ❓ /help - See a list of available commands from HQ
    ℹ️ /intel - Get the latest intel from HQ
    🤣 /joke - A much needed distraction in these dire times

OVER
"""


class HelpCommand(Command):
    async def handle(self, context: Context) -> None:
        command: str = context.message.text

        if command.lower().strip() == "/help":
            await context.send(HELP_MESSAGE)
            return


class IntelCommand(Command):
    async def handle(self, context: Context) -> None:
        command: str = context.message.text

        if command.lower().strip() == "/intel":
            intel = get_latest_intel()
            if not intel:
                await context.send(
                    "Connection lost with HQ. No intel available at the moment."
                )
                return
            await context.send(intel.description)


class JokeCommand(Command):
    async def handle(self, context: Context) -> None:
        command: str = context.message.text

        if command.lower().strip() == "/joke":
            joke = get_random_joke()
            if not joke:
                await context.send(
                    "Connection lost with HQ. No jokes available at the moment."
                )
                return
            await context.send(joke.description)


command_list: list[type[HelpCommand] | type[IntelCommand] | type[JokeCommand]] = [
    HelpCommand,
    IntelCommand,
    JokeCommand,
]
