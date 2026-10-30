#!/usr/bin/env python3
"""Validate required Telugu names in a lyric file and optional transliterations."""
import argparse
from pathlib import Path

REQUIRED_TELUGU = {
    "Telugu place name": "పెరిపి గ్రామం",
    "MPTC candidate Telugu name": "కొరాడ కోటేశ్వరరావు",
    "ZPTC candidate Telugu name": "వలిరెడ్డి శ్రీనివాస్ నాయుడు",
}
REQUIRED_ROMAN = {
    "Place transliteration": "Peripi Graamam",
    "MPTC transliteration": "Korada Koteswara Rao",
    "ZPTC transliteration": "Valireddy Srinivas Naidu",
}

def check(path: Path, phrases: dict[str, str]) -> list[str]:
    if not path.is_file():
        return [f"File not found: {path}"]
    content = path.read_text(encoding="utf-8")
    return [f"{path}: missing {label} ({phrase})" for label, phrase in phrases.items() if phrase not in content]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lyrics", nargs="?", default="lyrics/song_te.txt")
    parser.add_argument("--pronunciation", default="lyrics/pronunciation.txt", help="Romanized name guide")
    args = parser.parse_args()
    errors = check(Path(args.lyrics), REQUIRED_TELUGU)
    errors += check(Path(args.pronunciation), REQUIRED_ROMAN)
    if errors:
        print("SPELLING CHECK FAILED")
        print("\n".join(f" - {e}" for e in errors))
        raise SystemExit(1)
    print("Spelling check passed: all required Telugu names and romanized pronunciation cues are present.")
    print("Note: text validation cannot verify how a singer pronounces the names; listen to the final audio.")

if __name__ == "__main__":
    main()
