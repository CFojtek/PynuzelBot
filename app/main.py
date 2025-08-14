import logging
import os

from signalbot import SignalBot

from pynuzel_bot.commands import ForwardCommand, HelpCommand, IntelCommand, JokeCommand
from pynuzel_bot.env import load_secrets_to_env

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

load_secrets_to_env()
# Default to localhost if not provided
if not os.environ.get("SIGNAL_SERVICE"):
    os.environ["SIGNAL_SERVICE"] = "127.0.0.1:8080"


USER_CMDS = [HelpCommand, IntelCommand, JokeCommand]
ADMIN_CMDS = USER_CMDS + [ForwardCommand]


def main() -> None:
    try:
        signal_service = os.environ["SIGNAL_SERVICE"]
        phone_number = os.environ["PHONE_NUMBER"]
        groups = [os.environ["USER_GROUP"], os.environ["ADMIN_GROUP"]]

        bot: SignalBot = SignalBot(
            config={
                "signal_service": signal_service,
                "phone_number": phone_number,
            }
        )
        logging.info(
            f"Pynuzel bot initialized for phone number ending in {phone_number[-2:]} and groups {groups}"
        )

        # User commands can be used in user groups and replies will be send to the user group as well
        for cmd in USER_CMDS:
            bot.register(
                cmd(),
                contacts=False,
                groups=[os.environ["USER_GROUP"]],
            )
        # Admin commands can be used in admin groups and replies will be send to the user group
        for cmd in ADMIN_CMDS:
            bot.register(
                cmd(recipients=[os.environ["USER_GROUP"]]),
                contacts=False,
                groups=[os.environ["ADMIN_GROUP"]],
            )

        logging.info("Pynuzel bot commands registered successfully")
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
