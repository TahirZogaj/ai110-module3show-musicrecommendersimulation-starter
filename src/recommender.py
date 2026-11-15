import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Algorithm Recipe weights (see README "How The System Works")
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0    # max points for a perfect energy match
ACOUSTIC_WEIGHT = 0.5  # max points for acoustic fit

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv into a list of dicts, converting numeric columns to int/float."""
    int_fields = ["id"]
    float_fields = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # csv gives every value as text; convert numeric columns so we can do math later.
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song against the user's preferences and returns (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Rule 1: genre match (+2.0)
    if song["genre"].lower() == str(user_prefs.get("favorite_genre", "")).lower():
        score += GENRE_WEIGHT
        reasons.append(f"genre match: {song['genre']} (+{GENRE_WEIGHT:.1f})")

    # Rule 2: mood match (+1.0)
    if song["mood"].lower() == str(user_prefs.get("favorite_mood", "")).lower():
        score += MOOD_WEIGHT
        reasons.append(f"mood match: {song['mood']} (+{MOOD_WEIGHT:.1f})")

    # Rule 3: energy closeness (0 to +1.0). Rewards being NEAR the target, not just high or low.
    if "target_energy" in user_prefs:
        gap = abs(song["energy"] - user_prefs["target_energy"])
        energy_points = ENERGY_WEIGHT * (1 - gap)
        score += energy_points
        reasons.append(
            f"energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f} (+{energy_points:.2f})"
        )

    # Rule 4: acoustic fit (0 to +0.5)
    if "likes_acoustic" in user_prefs:
        if user_prefs["likes_acoustic"]:
            acoustic_points = ACOUSTIC_WEIGHT * song["acousticness"]
            label = "acoustic"
        else:
            acoustic_points = ACOUSTIC_WEIGHT * (1 - song["acousticness"])
            label = "non-acoustic"
        score += acoustic_points
        reasons.append(f"{label} fit (+{acoustic_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, sorts highest first, and returns the top k as (song, score, explanation)."""
    # Judge every song with score_song, keeping (song, score, explanation) together.
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    # sorted() returns a NEW list and leaves `songs` in its original CSV order.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
