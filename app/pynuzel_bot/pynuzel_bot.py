import logging

from signalbot import SignalBot

from pynuzel_bot.commands import command_list


class PynuzelBot:
    def __init__(self, signal_service: str, phone_number: str) -> None:
        self.signal_service: str = signal_service
        self.phone_number: str = phone_number

        self.bot: SignalBot = SignalBot(
            config={
                "signal_service": self.signal_service,
                "phone_number": self.phone_number,
                "storage": None,
            }
        )

        self.register_handlers()
        logging.info(f"Bot started for phone number ending in {phone_number[-2:]}")

    def register_handlers(self) -> None:
        for command in command_list:
            self.bot.register(command())

    def start(self) -> None:
        logging.info("Starting Pynuzel bot...")

        try:
            self.bot.start()
        except Exception:
            logging.error("Error starting Pynuzel bot")
            raise
