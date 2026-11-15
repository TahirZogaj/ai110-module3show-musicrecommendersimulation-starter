# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and YouTube combine two approaches. **Collaborative filtering** recommends what similar users liked, based on behavior such as likes, skips, replays and playlist adds. **Content-based filtering** recommends songs whose attributes, such as genre, mood, tempo and energy, resemble what the user already enjoys. These systems usually work in two stages: they first gather candidate songs, then rank them with a model that predicts what the user will engage with. My version is a small **content-based** recommender, because the dataset has song attributes but no listening history from other users. It prioritizes **genre first, then mood, then how close a song's energy is to the user's target**, so it favors songs that match the user's overall "vibe" rather than simply the loudest or calmest songs.

### Features used

**`Song`**
- `genre`: compared to the user's favorite genre (exact match)
- `mood`: compared to the user's favorite mood (exact match)
- `energy` (0–1): compared to the user's target energy by closeness
- `acousticness` (0–1): used as a small tiebreaker based on the user's acoustic preference
- `title`, `artist`: shown in results and explanations
- Loaded but not scored: `tempo_bpm`, `danceability` and `valence`. Tempo and danceability are strongly correlated with energy in this dataset (0.96 and 0.86), so scoring them would count the same signal twice.

**`UserProfile`**
- `favorite_genre`: e.g. `"pop"`
- `favorite_mood`: e.g. `"happy"`
- `target_energy`: e.g. `0.8`
- `likes_acoustic`: `True` / `False`

### Algorithm recipe

**Scoring rule (one song):**

| Rule | Points |
|---|---|
| Genre matches `favorite_genre` | +2.0 |
| Mood matches `favorite_mood` | +1.0 |
| Energy closeness: `1 − abs(song.energy − target_energy)` | up to +1.0 |
| Acoustic fit: `acousticness` if `likes_acoustic`, else `1 − acousticness` | up to +0.5 |

The maximum score is 4.5. Each rule that adds points also records a reason, such as "genre match (+2.0)", so every recommendation can be explained.

**Ranking rule (list of songs):** score every song, sort from highest to lowest score, and return the top `k`.

```
UserProfile + songs.csv → score each song → sort by score → top k + reasons
```

### Dataset and example profile

`data/songs.csv` was expanded from 10 to **20 songs** (17 genres, 16 moods). The new songs add genres and moods that were missing, such as metal, classical, folk, sad and angry, and include low-valence (dark) songs.

`src/main.py` runs two profiles. The default is an upbeat **pop/happy** listener:

```python
{"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.80, "likes_acoustic": False}
```

The second is a "late-night study" **lofi/chill** listener:

```python
{"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.40, "likes_acoustic": True}
```

Expected top 3 for lofi/chill: **Library Rain** (4.38), **Midnight Coding** (4.33), **Focus Flow** (3.39).

### Expected biases and limitations

- **Over-prioritizes genre.** A genre match (+2.0) is worth twice a mood match, so a same-genre song with the wrong mood can outrank a song that fits the mood perfectly. For a pop/happy user, "Gym Hero" (pop, *intense*) is expected to rank above "Rooftop Lights" (indie pop, *happy*).
- **Exact string matching is strict.** "indie pop" gets no credit for "pop", and "relaxed" or "peaceful" get no credit for "chill", even though they feel similar.
- **Sparse genres create a score cliff.** Most genres have only one song, so after the genre matches run out, the remaining songs are separated by tiny differences in energy and can be nearly tied.
- **No happy-vs-dark signal.** Valence isn't scored, so for a high-energy user, angry metal and festive Latin music score about the same.
- **Energy dominates the numeric score.** Energy, tempo, danceability and acousticness are highly correlated in this dataset, so the system mostly sees one dimension: calm vs intense.
- **Small, hand-made catalog.** 20 songs with made-up values reflect the dataset author's judgment about each genre's "typical" sound, not real listening data.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default **pop/happy** profile:

```
Loaded songs: 20

================================================================
Profile: Pop / Happy
  genre=pop  mood=happy  energy=0.80  acoustic=False
================================================================
1. Sunrise City — Neon Echo
   Score: 4.39 / 4.50   (pop, happy)
     • genre match: pop (+2.0)
     • mood match: happy (+1.0)
     • energy 0.82 vs target 0.80 (+0.98)
     • non-acoustic fit (+0.41)

2. Gym Hero — Max Pulse
   Score: 3.35 / 4.50   (pop, intense)
     • genre match: pop (+2.0)
     • energy 0.93 vs target 0.80 (+0.87)
     • non-acoustic fit (+0.47)

3. Rooftop Lights — Indigo Parade
   Score: 2.29 / 4.50   (indie pop, happy)
     • mood match: happy (+1.0)
     • energy 0.76 vs target 0.80 (+0.96)
     • non-acoustic fit (+0.33)

4. Concrete Crown — Mic Atlas
   Score: 1.44 / 4.50   (hip hop, confident)
     • energy 0.78 vs target 0.80 (+0.98)
     • non-acoustic fit (+0.46)

5. Storm Runner — Voltline
   Score: 1.34 / 4.50   (rock, intense)
     • energy 0.91 vs target 0.80 (+0.89)
     • non-acoustic fit (+0.45)
```

**Does this match expectations?** Mostly yes. Sunrise City is the only song that matches pop *and* happy, so it ranks #1 with a near-perfect score. Gym Hero (#2) beats Rooftop Lights (#3) because a genre match (+2.0) outweighs a mood match (+1.0), even though Rooftop Lights arguably fits a "happy" listener better. This is the genre bias predicted above. Ranks 4–5 have no genre or mood match and are ordered only by energy closeness.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



