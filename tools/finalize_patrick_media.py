#!/usr/bin/env python3
"""Apply the visual review, create service sets, and compress selected images."""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
REVIEW_ROOT = ROOT / "patrick-media-review"
MANIFEST_PATH = REVIEW_ROOT / "00-manifest" / "media-manifest.json"
ORIGINALS = REVIEW_ROOT / "01-all-originals"
KEEP_DIR = REVIEW_ROOT / "02-review" / "keep"
REJECT_DIR = REVIEW_ROOT / "02-review" / "do-not-use"
WEB_ALL = REVIEW_ROOT / "03-web-ready" / "all-keepers"
WEB_BY_SERVICE = REVIEW_ROOT / "03-web-ready" / "by-service"
REVIEW_SHEETS = REVIEW_ROOT / "00-manifest" / "decision-contact-sheets"

MAX_EDGE = 1600
WEBP_QUALITY = 78


KEEP_SERVICES = {
    1: ["steps-and-terraces", "dry-stone-walling", "bespoke-ironmongery"],
    2: ["dry-stone-walling", "bespoke-ironmongery"],
    4: ["paving-and-patios"],
    5: ["dry-stone-walling"],
    6: ["dry-stone-walling"],
    7: ["paving-and-patios", "landscaping", "groundworks"],
    8: ["lime-mortar-pointing"],
    10: ["steps-and-terraces", "dry-stone-walling", "landscaping"],
    11: ["landscaping", "paving-and-patios", "dry-stone-walling"],
    12: ["paving-and-patios", "groundworks"],
    13: ["paving-and-patios"],
    15: ["steps-and-terraces", "dry-stone-walling"],
    18: ["paving-and-patios", "landscaping", "dry-stone-walling"],
    19: ["paving-and-patios", "steps-and-terraces", "landscaping", "dry-stone-walling"],
    21: ["groundworks", "landscaping"],
    22: ["groundworks", "landscaping"],
    23: ["dry-stone-walling"],
    24: ["dry-stone-walling"],
    25: ["groundworks", "landscaping", "dry-stone-walling"],
    26: ["dry-stone-walling"],
    27: ["groundworks"],
    28: ["paving-and-patios", "steps-and-terraces", "landscaping", "dry-stone-walling"],
    29: ["paving-and-patios", "landscaping"],
    30: ["paving-and-patios", "landscaping", "dry-stone-walling"],
    32: ["paving-and-patios", "steps-and-terraces", "landscaping"],
    33: ["paving-and-patios", "steps-and-terraces", "landscaping"],
    35: ["landscaping", "dry-stone-walling"],
    36: ["dry-stone-walling", "landscaping"],
    37: ["dry-stone-walling"],
    38: ["landscaping", "dry-stone-walling"],
    39: ["landscaping", "dry-stone-walling", "steps-and-terraces"],
    40: ["steps-and-terraces", "dry-stone-walling", "landscaping", "paving-and-patios"],
    42: ["paving-and-patios", "landscaping", "dry-stone-walling"],
    43: ["paving-and-patios", "landscaping", "dry-stone-walling"],
    44: ["landscaping", "dry-stone-walling", "paving-and-patios"],
    45: ["steps-and-terraces", "dry-stone-walling", "landscaping"],
    46: ["landscaping", "dry-stone-walling", "steps-and-terraces"],
    49: ["landscaping", "dry-stone-walling"],
    51: ["landscaping", "dry-stone-walling"],
    61: ["dry-stone-walling"],
    63: ["dry-stone-walling"],
    64: ["dry-stone-walling"],
    68: ["paving-and-patios", "steps-and-terraces", "dry-stone-walling"],
    70: ["paving-and-patios", "steps-and-terraces", "dry-stone-walling"],
    71: ["paving-and-patios", "steps-and-terraces", "landscaping"],
    74: ["steps-and-terraces", "paving-and-patios", "dry-stone-walling", "bespoke-ironmongery"],
    75: ["paving-and-patios", "steps-and-terraces", "bespoke-ironmongery"],
    77: ["paving-and-patios", "landscaping", "steps-and-terraces"],
    78: ["paving-and-patios", "steps-and-terraces", "landscaping", "dry-stone-walling"],
    79: ["paving-and-patios", "landscaping", "dry-stone-walling"],
    81: ["paving-and-patios", "groundworks"],
    82: ["paving-and-patios", "landscaping", "dry-stone-walling"],
    94: ["lime-mortar-pointing"],
}

SMALL_OR_INCOMPLETE = {
    20, 31, 54, 59, 65, 66, 67, 80, 83, 84, 86, 87,
    91, 92, 93, 95,
}


def hardlink(source: Path, destination: Path) -> None:
    if not destination.exists():
        os.link(source, destination)


def web_filename(item: dict) -> str:
    return f"patrick-{item['sequence']:03d}.webp"


def compress(source: Path, destination: Path) -> None:
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        if max(image.size) > MAX_EDGE:
            scale = MAX_EDGE / max(image.size)
            image = image.resize(
                (round(image.width * scale), round(image.height * scale)),
                Image.Resampling.LANCZOS,
            )
        image.save(destination, "WEBP", quality=WEBP_QUALITY, method=6, optimize=True)


def build_sheets(items: list[dict], decision: str, colour: str) -> None:
    selected = [item for item in items if item["decision"] == decision]
    thumb_width, thumb_height, label_height = 340, 285, 38
    columns, rows = 4, 5
    per_sheet = columns * rows
    font = ImageFont.load_default(size=22)
    for page, start in enumerate(range(0, len(selected), per_sheet), 1):
        subset = selected[start : start + per_sheet]
        sheet = Image.new("RGB", (columns * thumb_width, rows * (thumb_height + label_height)), "#f3f1ea")
        draw = ImageDraw.Draw(sheet)
        for index, item in enumerate(subset):
            row, column = divmod(index, columns)
            x, y = column * thumb_width, row * (thumb_height + label_height)
            with Image.open(ORIGINALS / item["staged_filename"]) as opened:
                preview = ImageOps.contain(ImageOps.exif_transpose(opened).convert("RGB"), (thumb_width - 12, thumb_height - 12))
            sheet.paste(preview, (x + (thumb_width - preview.width) // 2, y + (thumb_height - preview.height) // 2))
            draw.rectangle((x, y + thumb_height, x + thumb_width, y + thumb_height + label_height), fill=colour)
            draw.text((x + 10, y + thumb_height + 7), f"{item['sequence']:03d}  {decision}", fill="white", font=font)
        sheet.save(REVIEW_SHEETS / f"{decision}-{page:02d}.jpg", quality=90, optimize=True)


def main() -> None:
    payload = json.loads(MANIFEST_PATH.read_text())
    items = payload["items"]
    for directory in (KEEP_DIR, REJECT_DIR, WEB_ALL, REVIEW_SHEETS):
        directory.mkdir(parents=True, exist_ok=True)

    for item in items:
        sequence = item["sequence"]
        source = ORIGINALS / item["staged_filename"]
        if sequence in KEEP_SERVICES:
            item["decision"] = "keep"
            item["services"] = KEEP_SERVICES[sequence]
            item["review_notes"] = "Strong, useful angle with distinct website value."
            rejected_copy = REJECT_DIR / item["staged_filename"]
            if rejected_copy.exists():
                rejected_copy.unlink()
            hardlink(source, KEEP_DIR / item["staged_filename"])

            compressed = WEB_ALL / web_filename(item)
            compress(source, compressed)
            item["web_filename"] = compressed.name
            item["web_size_bytes"] = compressed.stat().st_size
            for service in item["services"]:
                service_dir = WEB_BY_SERVICE / service
                service_dir.mkdir(parents=True, exist_ok=True)
                hardlink(compressed, service_dir / compressed.name)
        else:
            item["decision"] = "do-not-use"
            item["services"] = []
            if sequence in SMALL_OR_INCOMPLETE:
                item["review_notes"] = "Small repair, incomplete work, clutter, or weak website composition."
            else:
                item["review_notes"] = "Near-duplicate or weaker angle of a stronger selected image."
            selected_copy = KEEP_DIR / item["staged_filename"]
            if selected_copy.exists():
                selected_copy.unlink()
            hardlink(source, REJECT_DIR / item["staged_filename"])

    payload["review"] = {
        "keep_count": sum(item["decision"] == "keep" for item in items),
        "do_not_use_count": sum(item["decision"] == "do-not-use" for item in items),
        "compression": {"format": "WebP", "quality": WEBP_QUALITY, "max_edge_pixels": MAX_EDGE},
    }
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2) + "\n")

    csv_path = REVIEW_ROOT / "00-manifest" / "media-manifest.csv"
    fields = (
        "sequence", "staged_filename", "date_added", "width", "height", "file_size_bytes",
        "decision", "services", "review_notes", "web_filename", "web_size_bytes", "sha256", "dhash", "url",
    )
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in items:
            row = dict(item)
            row["services"] = ";".join(item["services"])
            writer.writerow({field: row.get(field, "") for field in fields})

    build_sheets(items, "keep", "#23513a")
    build_sheets(items, "do-not-use", "#7a2e2e")

    original_keep_bytes = sum(item["file_size_bytes"] for item in items if item["decision"] == "keep")
    web_bytes = sum(item.get("web_size_bytes", 0) for item in items if item["decision"] == "keep")
    report = {
        "all_originals": len(items),
        "keep": payload["review"]["keep_count"],
        "do_not_use": payload["review"]["do_not_use_count"],
        "keeper_original_bytes": original_keep_bytes,
        "web_ready_bytes": web_bytes,
        "reduction_percent": round((1 - web_bytes / original_keep_bytes) * 100, 1),
        "service_counts": {
            service: sum(service in item["services"] for item in items)
            for service in sorted({service for values in KEEP_SERVICES.values() for service in values})
        },
    }
    (REVIEW_ROOT / "00-manifest" / "review-summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
