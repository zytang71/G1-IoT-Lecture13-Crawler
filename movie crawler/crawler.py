import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

import bs4  # type: ignore
import requests

BASE_URL = "https://ssr1.scrape.center/page/{}"
OUTPUT_CSV = Path(__file__).parent / "movie.csv"


@dataclass
class Movie:
    title: str
    image: str
    rating: str
    genres: str


def fetch_page(page: int) -> str:
    url = BASE_URL.format(page)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text


def parse_page(html: str) -> List[Movie]:
    soup = bs4.BeautifulSoup(html, "html.parser")
    movies: List[Movie] = []
    for card in soup.select(".el-card"):
        title_tag = card.select_one(".m-b-sm")
        title = title_tag.get_text(strip=True) if title_tag else ""

        img_tag = card.select_one("img")
        image = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""

        rate_tag = card.select_one(".score")
        rating = rate_tag.get_text(strip=True) if rate_tag else ""

        genre_tags = card.select(".categories button span")
        genres = ", ".join(t.get_text(strip=True) for t in genre_tags)

        movies.append(Movie(title=title, image=image, rating=rating, genres=genres))
    return movies


def save_csv(rows: List[Movie], csv_path: Path = OUTPUT_CSV) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "image_url", "rating", "genres"])
        for m in rows:
            writer.writerow([m.title, m.image, m.rating, m.genres])


def main() -> None:
    all_movies: List[Movie] = []
    for page in range(1, 11):
        print(f"Fetching page {page}...", file=sys.stderr)
        html = fetch_page(page)
        all_movies.extend(parse_page(html))

    save_csv(all_movies)
    print(f"Saved {len(all_movies)} movies to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
