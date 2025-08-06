import random
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from pyairtable import Api
from pyairtable.formulas import IS_BEFORE, Field

from config import get_config

config = get_config()


@dataclass
class Intel:
    id: int
    release_date: datetime
    description: str


@dataclass
class Joke:
    id: int
    description: str


def get_latest_intel() -> Optional[Intel]:
    api = Api(config["AIRTABLE_TOKEN"])
    table = api.table(
        "appFvepvOj3Z8F58o",
        "Intel",
    )

    now = datetime.now(ZoneInfo("UTC"))
    formula = IS_BEFORE(Field("ReleaseDate"), now)
    records = table.all(
        formula=formula,
        sort=["-ReleaseDate"],
        max_records=1,
    )

    if not records:
        return None
    record = records[0]

    return Intel(
        id=record["fields"]["Id"],
        release_date=datetime.fromisoformat(record["fields"]["ReleaseDate"]),
        description=record["fields"]["Description"],
    )


def get_random_joke() -> Optional[Joke]:
    api = Api(config["AIRTABLE_TOKEN"])
    table = api.table(
        "appFvepvOj3Z8F58o",
        "Joke",
    )

    records = table.all()
    if not records:
        return None
    record = random.choice(records)

    return Joke(
        id=record["fields"]["Id"],
        description=record["fields"]["Description"],
    )
