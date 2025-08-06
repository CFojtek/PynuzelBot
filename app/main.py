import logging

from config import get_config
from pynuzel_bot import PynuzelBot

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)


def main() -> None:
    config = get_config()

    if not config["SIGNAL_SERVICE"]:
        raise ValueError("SIGNAL_SERVICE environment variable is required")
    if not config["SIGNAL_PHONE_NUMBER"]:
        raise ValueError("SIGNAL_PHONE_NUMBER environment variable is required")

    try:
        bot: PynuzelBot = PynuzelBot(
            config["SIGNAL_SERVICE"],
            config["SIGNAL_PHONE_NUMBER"],
        )
        bot.start()

    except KeyboardInterrupt:
        logging.info(msg="Bot stopped by user")
    except Exception as e:
        logging.error(msg=f"Bot went into an error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
