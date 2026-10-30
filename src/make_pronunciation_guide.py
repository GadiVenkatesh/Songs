#!/usr/bin/env python3
"""Print a clean singer cue sheet for the Peripi song."""
from pathlib import Path

GUIDE = """PERIPI TELUGU FOLK SONG — SINGER CUE SHEET

PLACE
Telugu: పెరిపి గ్రామం
Say: Pe-ri-pi GRAA-mam
Roman cue: Peripi Graamam

MPTC CANDIDATE
Telugu: కొరాడ కోటేశ్వరరావు
Roman cue: Ko-raa-da Ko-tesh-wa-ra-raa-vu
Sing in two parts: “Korada” / “Koteswara Rao”

ZPTC CANDIDATE
Telugu: వలిరెడ్డి శ్రీనివాస్ నాయుడు
Roman cue: Va-li-red-di Shree-ni-vaas Naa-yu-du
Sing in three parts: “Valireddy” / “Srinivas” / “Naidu”

RECORDING CHECK
[ ] Peripi Graamam is correct (not “Vilg Peripi”).
[ ] Korada Koteswara Rao is fully audible and correctly pronounced.
[ ] Valireddy Srinivas Naidu is fully audible and correctly pronounced.
[ ] Candidate names are not rushed or covered by drums.
[ ] Native Telugu speaker has checked the final audio.
"""
def main():
    output = Path("lyrics/singer_cue_sheet.txt")
    output.parent.mkdir(exist_ok=True)
    output.write_text(GUIDE, encoding="utf-8")
    print(GUIDE)
    print(f"Saved: {output}")
if __name__ == "__main__":
    main()
