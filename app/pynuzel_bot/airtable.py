import os
import random
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from pyairtable import Api
from pyairtable.formulas import IS_BEFORE, Field

AIRTABLE_BASE_ID = "appFvepvOj3Z8F58o"


@dataclass
class Intel:
    id: int
    release_date: datetime
    description: str


@dataclass
class Joke:
    id: int
    description: str


def authenticate() -> Api:
    api_token = os.environ.get("AIRTABLE_TOKEN")
    if not api_token:
        raise ValueError("AIRTABLE_TOKEN environment variable is required")

    return Api(api_token)


def get_latest_intel() -> Optional[Intel]:
    api = authenticate()
    table = api.table(
        AIRTABLE_BASE_ID,
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
    api = authenticate()
    table = api.table(
        AIRTABLE_BASE_ID,
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
