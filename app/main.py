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
    try:
        signal_service = os.environ["SIGNAL_SERVICE"]
        phone_number = os.environ["PHONE_NUMBER"]
        groups = [os.environ["USER_GROUP"], os.environ["ADMIN_GROUP"]]

        bot: SignalBot = initizialize_bot(
            signal_service=signal_service,
            phone_number=phone_number,
            groups=groups,
            storage=None,
        )

        logging.info("Starting Pynuzel bot...")
        bot.start()

    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except KeyError as e:
        logging.error(msg=f"Missing environment variable: {e}", exc_info=True)
        raise
    except Exception as e:
        logging.error(f"Bot went into an error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
