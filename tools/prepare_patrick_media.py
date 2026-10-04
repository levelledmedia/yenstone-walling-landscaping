#!/usr/bin/env python3
"""Stage Patrick's post-cutoff WhatsApp website media for review."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
REVIEW_ROOT = ROOT / "patrick-media-review"
MANIFEST_DIR = REVIEW_ROOT / "00-manifest"
ORIGINALS_DIR = REVIEW_ROOT / "01-all-originals"
REVIEW_KEEP_DIR = REVIEW_ROOT / "02-review" / "keep"
REVIEW_REJECT_DIR = REVIEW_ROOT / "02-review" / "do-not-use"
WEB_READY_DIR = REVIEW_ROOT / "03-web-ready" / "by-service"
CONTACT_SHEETS_DIR = REVIEW_ROOT / "00-manifest" / "contact-sheets"

SERVICES = (
    "landscaping",
    "dry-stone-walling",
    "steps-and-terraces",
    "paving-and-patios",
    "groundworks",
    "septic-tanks",
    "bespoke-ironmongery",
    "stone-cladding",
    "lime-mortar-pointing",
)

CUTOFF = "2026-10-03T14:21:34.000Z"


def load_messages(response_path: Path) -> list[dict]:
    wrapper = json.loads(response_path.read_text())
    payload = json.loads(wrapper["result"]["content"][0]["text"])
    return payload["data"]["messages"]["messages"]


def image_hash(image: Image.Image) -> str:
    gray = ImageOps.grayscale(image).resize((9, 8), Image.Resampling.LANCZOS)
    pixels = list(gray.getdata())
    bits = []
    for row in range(8):
        offset = row * 9
        bits.extend(pixels[offset + col] > pixels[offset + col + 1] for col in range(8))
    value = sum(int(bit) << index for index, bit in enumerate(bits))
    return f"{value:016x}"


def download(record: dict) -> dict:
    destination = ORIGINALS_DIR / record["staged_filename"]
    if not destination.exists():
        subprocess.run(
            [
                "curl", "--fail", "--location", "--silent", "--show-error",
                "--max-time", "60", "--output", str(destination), record["url"],
            ],
            check=True,
        )

    raw = destination.read_bytes()
    with Image.open(destination) as image:
        record.update(
            {
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "file_size_bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "dhash": image_hash(image),
            }
        )
    return record


def build_contact_sheets(records: list[dict]) -> None:
    thumb_width, thumb_height = 340, 285
    label_height = 36
    columns, rows = 4, 5
    per_sheet = columns * rows
    font = ImageFont.load_default(size=20)

    for page, start in enumerate(range(0, len(records), per_sheet), 1):
        page_records = records[start : start + per_sheet]
        sheet = Image.new(
            "RGB",
            (columns * thumb_width, rows * (thumb_height + label_height)),
            "#f2f0e9",
        )
        draw = ImageDraw.Draw(sheet)
        for index, record in enumerate(page_records):
            row, column = divmod(index, columns)
            x = column * thumb_width
            y = row * (thumb_height + label_height)
            with Image.open(ORIGINALS_DIR / record["staged_filename"]) as image:
                preview = ImageOps.contain(image.convert("RGB"), (thumb_width - 12, thumb_height - 12))
            px = x + (thumb_width - preview.width) // 2
            py = y + (thumb_height - preview.height) // 2
            sheet.paste(preview, (px, py))
            draw.rectangle((x, y + thumb_height, x + thumb_width, y + thumb_height + label_height), fill="#17241d")
            draw.text((x + 9, y + thumb_height + 7), record["staged_filename"], fill="white", font=font)
        sheet.save(CONTACT_SHEETS_DIR / f"contact-sheet-{page:02d}.jpg", quality=90, optimize=True)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: prepare_patrick_media.py PAGE1_RESPONSE PAGE2_RESPONSE")

    for directory in (
        MANIFEST_DIR,
        ORIGINALS_DIR,
        REVIEW_KEEP_DIR,
        REVIEW_REJECT_DIR,
        CONTACT_SHEETS_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)
    for service in SERVICES:
        (WEB_READY_DIR / service).mkdir(parents=True, exist_ok=True)

    messages = load_messages(Path(sys.argv[1])) + load_messages(Path(sys.argv[2]))
    messages.sort(key=lambda item: item["dateAdded"])

    records: list[dict] = []
    for message in messages:
        if message.get("direction") != "inbound" or message["dateAdded"] <= CUTOFF:
            continue
        for attachment in message.get("attachments") or []:
            extension = Path(urlparse(attachment).path).suffix.lower() or ".bin"
            if extension not in {".jpg", ".jpeg", ".png", ".webp", ".heic", ".gif"}:
                continue
            records.append(
                {
                    "sequence": len(records) + 1,
                    "message_id": message["id"],
                    "date_added": message["dateAdded"],
                    "body": message.get("body", ""),
                    "url": attachment,
                    "source_filename": Path(urlparse(attachment).path).name,
                    "staged_filename": f"{len(records) + 1:03d}-{Path(urlparse(attachment).path).name}",
                    "decision": "pending",
                    "services": [],
                    "review_notes": "",
                }
            )

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download, record) for record in records]
        records = [future.result() for future in as_completed(futures)]
    records.sort(key=lambda item: item["sequence"])

    manifest_path = MANIFEST_DIR / "media-manifest.json"
    manifest_path.write_text(json.dumps({"cutoff": CUTOFF, "count": len(records), "items": records}, indent=2) + "\n")

    csv_path = MANIFEST_DIR / "media-manifest.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=(
            "sequence", "staged_filename", "date_added", "width", "height",
            "file_size_bytes", "sha256", "dhash", "decision", "services", "review_notes", "url",
        ))
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["services"] = ";".join(record["services"])
            writer.writerow({key: row.get(key, "") for key in writer.fieldnames})

    build_contact_sheets(records)
    print(json.dumps({
        "review_root": str(REVIEW_ROOT),
        "downloaded": len(records),
        "total_bytes": sum(item["file_size_bytes"] for item in records),
        "contact_sheets": len(list(CONTACT_SHEETS_DIR.glob("contact-sheet-*.jpg"))),
    }))


if __name__ == "__main__":
    main()
