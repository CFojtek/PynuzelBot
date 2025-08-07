import logging
import os

from signalbot import SignalBot

from env import load_secrets_to_env
from pynuzel_bot.bot import initizialize_bot

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

load_secrets_to_env()
# Default to localhost if not provided
if not os.environ.get("SIGNAL_SERVICE"):
    os.environ["SIGNAL_SERVICE"] = "127.0.0.1:8080"


def main() -> None:
    signal_service = os.environ.get("SIGNAL_SERVICE")
    phone_number = os.environ.get("PHONE_NUMBER")

    if not signal_service:
        raise ValueError("SIGNAL_SERVICE environment variable is required")
    if not phone_number:
        raise ValueError("PHONE_NUMBER environment variable is required")

    try:
        bot: SignalBot = initizialize_bot(
            signal_service=signal_service, phone_number=phone_number, storage=None
        )
        bot.start()

    except KeyboardInterrupt:
        logging.info(msg="Bot stopped by user")
    except Exception as e:
        logging.error(msg=f"Bot went into an error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
