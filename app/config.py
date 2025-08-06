import json

config = None


def get_config() -> dict[str, str]:
    global config

    try:
        if config is not None:
            return config

        with open("docker.secrets.json", "r") as f:
            config = json.load(f)
        return config

    except Exception as e:
        raise RuntimeError(f"Failed to load configuration: {e}")
