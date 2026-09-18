#!/usr/bin/env python3
"""Add one YouTube Short to the generated content catalog."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import parse_qs, urlparse


def normalize_name(value: str) -> str:
    return " ".join(value.strip().lower().split())


def slugify(value: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    if not slug:
        raise ValueError("The animal name does not produce a usable id.")
    return slug


def youtube_id(url: str) -> str:
    parsed = urlparse(url.strip())
    hostname = (parsed.hostname or "").lower()
    video_id = ""

    if hostname in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/")[0]
    elif hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        path_parts = [part for part in parsed.path.split("/") if part]
        if len(path_parts) >= 2 and path_parts[0] in {"shorts", "embed"}:
            video_id = path_parts[1]
        elif parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]

    if not re.fullmatch(r"[A-Za-z0-9_-]{6,20}", video_id):
        raise ValueError("Enter a valid youtube.com/shorts or youtu.be URL.")
    return video_id


def add_clip(catalog: dict, animal_name: str, short_url: str) -> dict:
    name = normalize_name(animal_name)
    if not name:
        raise ValueError("The animal name must not be empty.")

    source_id = youtube_id(short_url)
    animals = catalog.setdefault("animals", [])

    for animal in animals:
        for source in animal.get("sources", []):
            if source.get("youtubeId") == source_id:
                raise ValueError(f"YouTube video {source_id} is already in the catalog.")

    animal = next((item for item in animals if item.get("name") == name), None)
    if animal is None:
        animal = {"id": slugify(name), "name": name, "sources": []}
        if any(item.get("id") == animal["id"] for item in animals):
            raise ValueError(f"The generated animal id {animal['id']!r} already exists.")
        animals.append(animal)

    animal.setdefault("sources", []).append(
        {
            "youtubeId": source_id,
            "url": f"https://www.youtube.com/shorts/{source_id}",
        }
    )
    animals.sort(key=lambda item: item["name"])
    return catalog


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--animal", required=True)
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    catalog = json.loads(args.catalog.read_text())
    updated = add_clip(catalog, args.animal, args.url)
    args.catalog.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
