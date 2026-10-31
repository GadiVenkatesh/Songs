#!/usr/bin/env python3
"""Generate a Telugu spoken announcement from a template and dynamic fields.

Uses edge-tts (Microsoft Edge's hosted neural TTS service). Internet is required.
This is text-to-speech, not singing/music generation.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path
from string import Formatter

import edge_tts

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "templates" / "announcement.txt"
DEFAULT_CONFIG = ROOT / "config" / "announcement.json"
DEFAULT_OUTPUT = ROOT / "output" / "announcement.mp3"
DEFAULT_VOICE = "te-IN-ShrutiNeural"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return data


def ask_if_missing(label: str, current: str) -> str:
    prompt = f"{label} [{current}]: " if current else f"{label}: "
    entered = input(prompt).strip()
    return entered or current


def collect_values(config: dict, interactive: bool) -> dict[str, str]:
    fields = {
        "place": "Place / village name",
        "area": "Area / mandal name",
        "person_1": "Person or organization name (optional)",
        "person_2": "Additional name (optional)",
        "announcement": "Announcement text",
    }
    values: dict[str, str] = {}
    for key, label in fields.items():
        value = str(config.get(key, "")).strip()
        if interactive:
            value = ask_if_missing(label, value)
        values[key] = value
    return values


def render_template(template: str, values: dict[str, str], pronunciation: dict[str, str]) -> str:
    # Keep name spelling under user control. Only explicit pronunciation mappings are applied.
    rendered = template.format_map({key: value for key, value in values.items()})
    for original, spoken_form in pronunciation.items():
        if original:
            rendered = rendered.replace(original, str(spoken_form))
    rendered = re.sub(r"[ \t]+", " ", rendered)
    rendered = re.sub(r"\n{3,}", "\n\n", rendered).strip()
    if not rendered:
        raise ValueError("Rendered announcement is empty.")
    return rendered


async def synthesize(text: str, voice: str, output: Path, rate: str, pitch: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    communicator = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    await communicator.save(str(output))


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Telugu spoken announcement MP3.")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Edge TTS voice, e.g. te-IN-ShrutiNeural")
    parser.add_argument("--rate", default="+0%", help="Speech rate, e.g. -8%% or +5%%")
    parser.add_argument("--pitch", default="+0Hz", help="Pitch, e.g. -2Hz or +2Hz")
    parser.add_argument("--non-interactive", action="store_true", help="Use values from config without prompts")
    args = parser.parse_args()

    try:
        if not args.template.is_file():
            raise FileNotFoundError(f"Template not found: {args.template}")
        template = args.template.read_text(encoding="utf-8")
        config = load_json(args.config)
        values = collect_values(config, interactive=not args.non_interactive)

        required = {field_name for _, field_name, _, _ in Formatter().parse(template) if field_name}
        missing = sorted(required - values.keys())
        if missing:
            raise ValueError("Unknown template placeholders: " + ", ".join(missing))
        empty = [key for key in required if not values.get(key, "").strip()]
        if empty:
            raise ValueError("Missing values for: " + ", ".join(sorted(empty)))

        pronunciation = config.get("pronunciation_overrides", {})
        if not isinstance(pronunciation, dict):
            raise ValueError("'pronunciation_overrides' must be a JSON object.")
        final_text = render_template(template, values, pronunciation)

        print("\n--- Text to be spoken ---\n")
        print(final_text)
        confirm = "y"
        if not args.non_interactive:
            confirm = input("\nGenerate MP3 with this text? [Y/n]: ").strip().lower()
        if confirm in {"n", "no"}:
            print("Cancelled. No audio generated.")
            return 0

        asyncio.run(synthesize(final_text, args.voice, args.output, args.rate, args.pitch))
        transcript_path = args.output.with_suffix(".txt")
        transcript_path.write_text(final_text + "\n", encoding="utf-8")
        print(f"\nAudio saved: {args.output}")
        print(f"Transcript saved: {transcript_path}")
        print("Review the generated audio and pronunciation before sharing.")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"TTS request failed: {exc}", file=sys.stderr)
        print("Check internet access and confirm the selected voice is available.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
