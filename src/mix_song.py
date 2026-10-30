#!/usr/bin/env python3
"""Mix a vocal stem and an instrumental stem into a final MP3.

Requires FFmpeg installed and available on PATH. This script does not synthesize singing;
it mixes already-recorded/generated audio stems.
"""
import argparse
from pathlib import Path
from pydub import AudioSegment
from pydub.effects import normalize

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vocal", required=True, help="Vocal stem (WAV/MP3)")
    parser.add_argument("--instrumental", required=True, help="Instrumental stem (WAV/MP3)")
    parser.add_argument("--output", default="peripi-final.mp3", help="Output MP3 path")
    parser.add_argument("--vocal-db", type=float, default=1.0, help="Vocal gain in dB")
    parser.add_argument("--music-db", type=float, default=-5.0, help="Instrumental gain in dB")
    parser.add_argument("--target-seconds", type=int, default=120, help="Target duration; 0 keeps full duration")
    args = parser.parse_args()

    vocal_path, music_path = Path(args.vocal), Path(args.instrumental)
    if not vocal_path.is_file():
        parser.error(f"Vocal file not found: {vocal_path}")
    if not music_path.is_file():
        parser.error(f"Instrumental file not found: {music_path}")

    vocal = AudioSegment.from_file(vocal_path).set_channels(2).set_frame_rate(44100)
    music = AudioSegment.from_file(music_path).set_channels(2).set_frame_rate(44100)

    target_ms = args.target_seconds * 1000 if args.target_seconds > 0 else max(len(vocal), len(music))
    if len(music) < target_ms:
        repeats = (target_ms // max(1, len(music))) + 1
        music = (music * repeats)[:target_ms]
    else:
        music = music[:target_ms]

    if len(vocal) < target_ms:
        vocal += AudioSegment.silent(duration=target_ms - len(vocal), frame_rate=44100)
    else:
        vocal = vocal[:target_ms]

    mixed = music.apply_gain(args.music_db).overlay(vocal.apply_gain(args.vocal_db))
    mixed = normalize(mixed, headroom=1.0)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    mixed.export(out, format="mp3", bitrate="192k")
    print(f"Created: {out.resolve()}")
    print(f"Duration: {len(mixed)/1000:.1f} seconds")
    print("QC reminder: listen for name pronunciation, clipped syllables, and vocals buried under percussion.")

if __name__ == "__main__":
    main()
