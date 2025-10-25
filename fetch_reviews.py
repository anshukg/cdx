"""Fetch all Google Play reviews for specified app."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from google_play_scraper import Sort, reviews_all


def fetch_all_reviews(app_id: str, lang: str = "en", country: str = "in"):
    """Fetch all reviews for an app from the Google Play Store."""

    return reviews_all(
        app_id,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        sleep_milliseconds=0,
    )


def _json_serializer(obj: Any) -> Any:
    """Convert objects unsupported by :mod:`json` into serialisable types."""

    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python fetch_reviews.py <app_id> [<output_json_path>]")
        return 1

    app_id = argv[1]
    output_path = Path(argv[2]) if len(argv) > 2 else Path("reviews.json")

    reviews = fetch_all_reviews(app_id)

    with output_path.open("w", encoding="utf-8") as fp:
        json.dump(reviews, fp, ensure_ascii=False, indent=2, default=_json_serializer)

    print(f"Saved {len(reviews)} reviews to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
