import logging
from typing import Optional

from signalbot import SignalBot

from pynuzel_bot.commands import command_list


def initizialize_bot(
    signal_service: str, phone_number: str, storage: Optional[str] = None
) -> SignalBot:
    bot: SignalBot = SignalBot(
        config={
            "signal_service": signal_service,
            "phone_number": phone_number,
            "storage": storage,
        }
    )
    for command in command_list:
        bot.register(command())

    logging.info(
        f"Pynuzel bot initialized for phone number ending in {phone_number[-2:]}"
    )
    return bot


def start_bot(bot: SignalBot) -> None:
    logging.info("Starting Pynuzel bot...")
    try:
        bot.start()
    except Exception:
        logging.error("Error starting Pynuzel bot")
        raise
