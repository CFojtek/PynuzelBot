import logging
from typing import Optional

from signalbot import SignalBot

from pynuzel_bot.commands import command_list


def initizialize_bot(
    signal_service: str,
    phone_number: str,
    groups: list[str],
    storage: Optional[str] = None,
) -> SignalBot:
    bot: SignalBot = SignalBot(
        config={
            "signal_service": signal_service,
            "phone_number": phone_number,
            "storage": storage,
        }
    )

    for command in command_list:
        bot.register(
            command(),
            contacts=False,
            groups=groups,
        )

    logging.info(
        f"Pynuzel bot initialized for phone number ending in {phone_number[-2:]} and groups {groups}"
    )
    return bot
