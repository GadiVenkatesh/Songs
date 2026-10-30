# Peripi Telugu Folk Song Studio

A small toolkit for preparing an original Telugu folk campaign song for Peripi Gramam. It includes Telugu lyrics, pronunciation notes, music-generation prompts, and Python utilities to validate lyrics and mix existing vocal and instrumental stems.

## Song brief
- Place: పెరిపి గ్రామం — Peripi Graamam
- MPTC candidate: కొరాడ కోటేశ్వరరావు — Korada Koteswara Rao
- ZPTC candidate: వలిరెడ్డి శ్రీనివాస్ నాయుడు — Valireddy Srinivas Naidu
- Style: upbeat Andhra folk with dappu, tappeta, hand claps, and nadaswaram accents
- Target: about 2 minutes, male/female call-and-response duet

## Files
- `lyrics/song_te.txt` — Telugu lyrics with singer cues
- `lyrics/pronunciation.txt` — Romanized pronunciation guide
- `prompts/music_prompt.txt` — prompt for a full-song generator
- `prompts/vocal_prompt.txt` — prompt for a vocal/stem workflow
- `src/validate_lyrics.py` — checks required names in the lyrics
- `src/make_pronunciation_guide.py` — prints a singer cue sheet
- `src/mix_song.py` — mixes existing vocal and instrumental stems into MP3

## Workflow
1. Review the lyrics and pronunciation guide with a Telugu speaker.
2. Use the music prompt in a Telugu-capable music generator or record the vocals separately.
3. Install FFmpeg and run `pip install -r requirements.txt`.
4. Mix stems: `python src/mix_song.py --vocal vocal.wav --instrumental instrumental.wav --output peripi-final.mp3`
5. Listen carefully and verify all candidate names before publishing.

**Important:** Python can validate spellings and mix existing audio stems, but it does not generate professional singing or guarantee correct sung pronunciation. The music-generation service previously attempted requires an active subscription.
