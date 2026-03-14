from dataclasses import dataclass
from typing import Dict
import redis


@dataclass
class Movie:
    title: str
    director: str
    year: int
    genre: str
    rating: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "director": self.director,
            "year": str(self.year),
            "genre": self.genre,
            "rating": self.rating,
        }

    @classmethod
    def from_dict(cls, data: Dict[bytes, bytes]) -> "Movie":
        decoded = {k.decode(): v.decode() for k, v in data.items()}

        return cls(
            title=decoded.get("title", ""),
            director=decoded.get("director", ""),
            year=int(decoded.get("year", "0")),
            genre=decoded.get("genre", ""),
            rating=decoded.get("rating", ""),
        )


REDIS_KEY_BASE = "movie"


def main() -> None:

    # 1. Koneksi ke Redis
    r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=False)

    # 2. Data film yang akan disimpan
    movies = [
        Movie("Avengers: Endgame", "Anthony Russo", 2019, "Action", "8.4"),
        Movie("Inception", "Christopher Nolan", 2010, "Sci-Fi", "8.8"),
        Movie("Parasite", "Bong Joon-ho", 2019, "Drama", "8.6"),
        Movie("Interstellar", "Christopher Nolan", 2014, "Sci-Fi", "8.7"),
        Movie("The Dark Knight", "Christopher Nolan", 2008, "Action", "9.0"),
    ]

    # 3. Menyimpan data film ke Redis
    for idx, movie in enumerate(movies, start=1):
        key = f"{REDIS_KEY_BASE}:{idx}"
        r.hset(key, mapping=movie.to_dict())

    # 4. Membaca kembali dari Redis
    print("Data Film dari Redis:")

    for idx in range(1, len(movies) + 1):
        key = f"{REDIS_KEY_BASE}:{idx}"
        stored = r.hgetall(key)
        loaded_movie = Movie.from_dict(stored)

        print(f"\n-- Film #{idx} --")
        print(f"Judul     : {loaded_movie.title}")
        print(f"Director  : {loaded_movie.director}")
        print(f"Tahun     : {loaded_movie.year}")
        print(f"Genre     : {loaded_movie.genre}")
        print(f"Rating    : {loaded_movie.rating}")


if __name__ == "__main__":
    main()