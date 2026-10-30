# Peripi Telugu Folk Song Studio

A toolkit for preparing an original Telugu folk campaign song for Peripi Gramam. Includes Telugu lyrics, pronunciation notes, generation prompts, and Python utilities to validate names and mix audio.

## Song brief
- Place: పెరిపి గ్రామం — Peripi Graamam
- MPTC candidate: కొరాడ కోటేశ్వరరావు — Korada Koteswara Rao
- ZPTC candidate: వలిరెడ్డి శ్రీనివాస్ నాయుడు — Valireddy Srinivas Naidu
- Style: upbeat Andhra folk with dappu/tappeta-inspired percussion, hand claps and call-and-response
- Target duration: about 2 minutes

## Current demo status
- The downloadable project ZIP contains `assets/peripi_folk_campaign_instrumental_demo.mp3`, an original instrumental demo, plus a playable vocal-guide MP3.
- `src/create_vocal_guide_demo.py` adds a rough spoken Telugu guide using the local eSpeak `te` test voice. It is useful for timing and checking name placement, but it is **not a natural sung duet** and the test voice may pronounce Telugu imperfectly.
- The binary audio is provided in the project ZIP rather than committed directly to this GitHub repository. Download the ZIP and extract it before running the script.

## Files
- `lyrics/song_te.txt` — Telugu lyrics with singer cues
- `lyrics/pronunciation.txt` — Romanized pronunciation guide
- `prompts/music_prompt.txt` — prompt for a full-song generator
- `prompts/vocal_prompt.txt` — prompt for a vocal-stem workflow
- `src/validate_lyrics.py` — checks required Telugu names and romanized cues
- `src/make_pronunciation_guide.py` — prints a singer cue sheet
- `src/mix_song.py` — mixes existing vocal and instrumental stems into MP3
- `src/create_vocal_guide_demo.py` — builds the rough spoken-guide demo

## Run locally
Requires Python, FFmpeg, and eSpeak with the `te` voice available. Install dependencies:

```bash
pip install -r requirements.txt
python src/validate_lyrics.py lyrics/song_te.txt
python src/make_pronunciation_guide.py
python src/create_vocal_guide_demo.py
```

The demo script writes `peripi_campaign_vocal_guide_demo.mp3` and `peripi_telugu_spoken_guide.wav` in the project root.

To mix real or generated vocals instead:

```bash
python src/mix_song.py --vocal vocal.wav --instrumental assets/peripi_folk_campaign_instrumental_demo.mp3 --output peripi-final.mp3
```

**Licensing note:** This project uses original lyrics and a programmatically created instrumental demo. Verify the license of any external model, voice, or audio asset you add, including the model weights, before using it in a public campaign.
