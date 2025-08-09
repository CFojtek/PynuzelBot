import os
import random
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union
from zoneinfo import ZoneInfo

from pyairtable import Api
from pyairtable.api.table import Table
from pyairtable.formulas import IS_BEFORE, Field


@dataclass
class HelpMessage:
    id: int
    text: str


@dataclass
class IntelMessage:
    id: int
    release_date: datetime
    text: str


@dataclass
class JokeMessage:
    id: int
    text: str


Message = Union[HelpMessage, IntelMessage, JokeMessage]


def authenticate() -> Api:
    api_token = os.environ.get("AIRTABLE_TOKEN")
    if not api_token:
        raise ValueError("AIRTABLE_TOKEN environment variable is required")

    return Api(api_token)


def get_table(context: Api, table_name: str) -> Table:
    base_id = os.environ.get("AIRTABLE_BASE_ID")
    if not base_id:
        raise ValueError("AIRTABLE_BASE_ID environment variable is required")

    return context.table(
        base_id,
        table_name,
    )


def get_help_message() -> Optional[HelpMessage]:
    context = authenticate()
    table = get_table(context, "Help")

    records = table.all(max_records=1)
    if not records:
        return None
    record = records[0]

    return HelpMessage(
        id=record["fields"]["Id"],
        text=record["fields"]["Text"],
    )


def get_latest_intel() -> Optional[IntelMessage]:
    context = authenticate()
    table = get_table(context, "Intel")

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

    return IntelMessage(
        id=record["fields"]["Id"],
        release_date=datetime.fromisoformat(record["fields"]["ReleaseDate"]),
        text=record["fields"]["Text"],
    )


def get_random_joke() -> Optional[JokeMessage]:
    context = authenticate()
    table = get_table(context, "Joke")

    records = table.all()
    if not records:
        return None
    record = random.choice(records)

    return JokeMessage(
        id=record["fields"]["Id"],
        text=record["fields"]["Text"],
    )
