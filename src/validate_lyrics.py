#!/usr/bin/env python3
"""Validate required place/candidate spellings in a Telugu lyric file."""
import argparse
from pathlib import Path

REQUIRED = {
    "Telugu place name": "పెరిపి గ్రామం",
    "MPTC candidate Telugu name": "కొరాడ కోటేశ్వరరావు",
    "ZPTC candidate Telugu name": "వలిరెడ్డి శ్రీనివాస్ నాయుడు",
}
ROMAN = {
    "Place transliteration": "Peripi Graamam",
    "MPTC transliteration": "Korada Koteswara Rao",
    "ZPTC transliteration": "Valireddy Srinivas Naidu",
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", default="lyrics/song_te.txt")
    args = parser.parse_args()
    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"ERROR: file not found: {path}")
    content = path.read_text(encoding="utf-8")
    missing = [label for label, phrase in {**REQUIRED, **ROMAN}.items() if phrase not in content]
    if missing:
        print("SPELLING CHECK FAILED")
        for label in missing:
            print(f" - Missing exact phrase: {label}")
        raise SystemExit(1)
    print("Spelling check passed: all required Telugu and Romanized names are present.")
    print("Note: text validation cannot verify how an AI singer pronounces the names; listen to the rendered audio.")
if __name__ == "__main__":
    main()
