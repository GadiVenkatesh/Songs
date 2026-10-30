#!/usr/bin/env python3
"""Create a rough spoken Telugu guide over the instrumental demo.

This uses the local eSpeak Telugu test voice, which is not a singing voice and may
pronounce Telugu imperfectly. It is for timing/name placement only.
Requires FFmpeg and pydub.
"""
from pathlib import Path
import subprocess
import tempfile
from pydub import AudioSegment, effects

BASE = Path(__file__).resolve().parents[1]
INSTRUMENTAL = BASE / "assets" / "peripi_folk_campaign_instrumental_demo.mp3"
LINES = [
    (3, "అయ్యా ఓయ్ పెరిపి గ్రామమా! మన ఊరి మాట, మన ఊరి పాట!"),
    (12, "పెరిపి గ్రామం పండుగలా, పల్లెంతా సందడిరా!"),
    (20, "కొరాడ కోటేశ్వరరావు! MPTC అభ్యర్థి కొరాడ కోటేశ్వరరావు!"),
    (30, "పెరిపి, పెరిపి, మన ఊరి గళమిదే! కలిసి నడిచే అడుగులే మన బలమిదే!"),
    (40, "వలిరెడ్డి శ్రీనివాస్ నాయుడు! ZPTC అభ్యర్థి వలిరెడ్డి శ్రీనివాస్ నాయుడు!"),
    (52, "పొలాల గాలి పలకరిస్తే, పల్లె పాట మొదలయ్యే!"),
    (62, "పక్కపక్కన చేతులు కలిస్తే, కొత్త దారి కనిపించే!"),
    (72, "మన ఊరి ఆశలన్నీ, మనసులోనే దాచుకోం! మంచి మాట, మంచి పని, అందరం కలిసి కోరుకుందాం!"),
    (84, "అక్కచెల్లెళ్ల నవ్వుల్లోనూ, అన్నదమ్ముల మాటల్లోనూ!"),
    (94, "మన MPTC అభ్యర్థి కొరాడ కోటేశ్వరరావు!"),
    (102, "మన ZPTC అభ్యర్థి వలిరెడ్డి శ్రీనివాస్ నాయుడు!"),
    (110, "పెరిపి గ్రామం, మన ఊరి గౌరవం! కొరాడ కోటేశ్వరరావు! వలిరెడ్డి శ్రీనివాస్ నాయుడు! జై జై పెరిపి!"),
]

def main():
    if not INSTRUMENTAL.is_file():
        raise SystemExit(f"Missing instrumental asset: {INSTRUMENTAL}")
    instrumental = AudioSegment.from_file(INSTRUMENTAL).set_frame_rate(44100).set_channels(2)
    voice_track = AudioSegment.silent(duration=len(instrumental), frame_rate=44100).set_channels(2)
    with tempfile.TemporaryDirectory() as tmp:
        for i, (seconds, text) in enumerate(LINES):
            wav = Path(tmp) / f"line{i}.wav"
            subprocess.run(["espeak", "-v", "te", "-s", "132", "-p", "48", "-a", "165", "-w", str(wav), text], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            clip = effects.normalize(AudioSegment.from_file(wav).set_frame_rate(44100).set_channels(2), headroom=3.0).apply_gain(3)
            clip = clip.fade_in(12).fade_out(100)
            pos = seconds * 1000
            clip = clip[:max(0, len(voice_track) - pos)]
            if len(clip):
                voice_track = voice_track.overlay(clip, position=pos)
    mixed = effects.normalize(instrumental.apply_gain(-5).overlay(voice_track), headroom=1.5)
    mixed.export(BASE / "peripi_campaign_vocal_guide_demo.mp3", format="mp3", bitrate="192k")
    voice_track.export(BASE / "peripi_telugu_spoken_guide.wav", format="wav")
    print("Created rough vocal guide demo. Please review pronunciation with a native Telugu speaker.")

if __name__ == "__main__":
    main()
