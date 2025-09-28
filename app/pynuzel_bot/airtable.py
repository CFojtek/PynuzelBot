import logging
import os
import random
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Union

from fuzzywuzzy import process
from pyairtable import Api
from pyairtable.api.table import Table
from pyairtable.api.types import RecordDict
from pyairtable.formulas import IS_BEFORE, Field

from pynuzel_bot.cache import timed_lru_cache


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
    subject: Optional[str] = None


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

    now = datetime.now(timezone.utc)
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
        subject=record["fields"].get("Subject"),
    )


def get_random_joke_by_subjects(subjects: list[str]) -> Optional[JokeMessage]:
    unique_subjects = get_unique_joke_subjects()
    fuzzy_subjects = [
        result[0]
        for subject in subjects
        if (result := process.extractOne(subject, unique_subjects)) is not None
    ]
    logging.warning(fuzzy_subjects)
    records = get_records_by_field_values("Joke", "Subject", fuzzy_subjects)
    if not records:
        return None
    logging.warning(records)
    record = random.choice(records)
    logging.warning(record)

    return JokeMessage(
        id=record["fields"]["Id"],
        text=record["fields"]["Text"],
        subject=record["fields"].get("Subject"),
    )


@timed_lru_cache(seconds=600)
def get_unique_joke_subjects() -> Optional[list[str]]:
    """Fetch unique joke subjects using a timed cache to reduce API calls."""
    context = authenticate()
    table = get_table(context, "Joke")

    records = table.all()
    if not records:
        return None

    subjects = {
        record["fields"]["Subject"]
        for record in records
        if "Subject" in record["fields"]
    }
    return list(subjects)


def get_records_by_field_values(
    table_name: str, field_name: str, values: list[str]
) -> list[RecordDict]:
    context = authenticate()
    table = get_table(context, table_name)
    condition = [f'{{{field_name}}}="{v}"' for v in values]
    formula = f"OR({', '.join(condition)})"
    logging.warning(formula)
    records = table.all(formula=formula)
    return records
