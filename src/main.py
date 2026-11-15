"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:  python -m src.main
"""

try:
    from src.recommender import load_songs, recommend_songs  # python -m src.main
except ImportError:
    from recommender import load_songs, recommend_songs  # python src/main.py


# Taste profiles. Keys match the UserProfile dataclass fields in recommender.py.
PROFILES = {
    # --- Core profiles ---
    # Default profile: upbeat, energetic pop listener.
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "likes_acoustic": False,
    },
    # "Late-night study" listener who wants calm, acoustic, chill lofi.
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
    },
    # --- Adversarial / edge-case profiles ---
    # Conflicting: sad mood but very high energy (sad songs in the catalog are calm).
    "EDGE: Sad but Hyped": {
        "favorite_genre": "edm",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "likes_acoustic": False,
    },
    # Conflicting: wants metal energy but also acoustic sound.
    "EDGE: Acoustic Headbanger": {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 0.95,
        "likes_acoustic": True,
    },
    # Genre and mood that don't exist in the catalog.
    "EDGE: Ghost Genre": {
        "favorite_genre": "k-pop",
        "favorite_mood": "euphoric",
        "target_energy": 0.50,
        "likes_acoustic": False,
    },
    # Invalid input: energy outside the 0-1 range.
    "EDGE: Out-of-Range Energy": {
        "favorite_genre": "classical",
        "favorite_mood": "peaceful",
        "target_energy": 1.50,
        "likes_acoustic": True,
    },
}

WIDTH = 64


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Prints one profile's top-k results as a readable block."""
    print("=" * WIDTH)
    print(f"Profile: {name}")
    print(
        f"  genre={user_prefs['favorite_genre']}  mood={user_prefs['favorite_mood']}  "
        f"energy={user_prefs['target_energy']:.2f}  acoustic={user_prefs['likes_acoustic']}"
    )
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f} / 4.50   ({song['genre']}, {song['mood']})")
        for reason in explanation.split("; "):
            print(f"     • {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
