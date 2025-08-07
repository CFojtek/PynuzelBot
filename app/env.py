import json
import os


def load_secrets_to_env() -> None:
    if "ENV" in os.environ:
        return

    if os.path.exists("secrets.json"):
        with open("secrets.json", "r") as f:
            secrets = json.load(f)
            for key, value in secrets.items():
                os.environ[key] = str(value)
    else:
        raise FileNotFoundError(
            "secrets.json file not found, or environment variables not set."
        )
