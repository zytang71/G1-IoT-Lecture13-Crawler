import json
import sqlite3
from pathlib import Path
from typing import Dict, List

BASE_DIR = Path(__file__).parent
RAW_PATH = BASE_DIR / "weather_raw.json"
DB_PATH = BASE_DIR / "data.db"


def _merge_daily(entries: Dict[str, Dict], daily: List[Dict], key: str) -> None:
    """Merge daily readings into a date-keyed dictionary."""
    for item in daily or []:
        date = item.get("dataDate")
        if not date:
            continue
        bucket = entries.setdefault(date, {})
        bucket[key] = item


def parse_weather(raw_path: Path = RAW_PATH) -> List[Dict]:
    """Parse the CWA agrWeatherForecasts JSON into normalized rows."""
    data = json.loads(raw_path.read_text(encoding="utf-8"))
    forecasts = (
        data["cwaopendata"]["resources"]["resource"]["data"]["agrWeatherForecasts"][
            "weatherForecasts"
        ]["location"]
    )

    rows: List[Dict] = []
    for location in forecasts:
        name = location.get("locationName", "")
        elements = location.get("weatherElements", {})
        by_date: Dict[str, Dict] = {}

        _merge_daily(by_date, elements.get("MinT", {}).get("daily", []), "min")
        _merge_daily(by_date, elements.get("MaxT", {}).get("daily", []), "max")
        _merge_daily(by_date, elements.get("Wx", {}).get("daily", []), "wx")

        for date, parts in by_date.items():
            rows.append(
                {
                    "location": name,
                    "date": date,
                    "min_temp": float(parts.get("min", {}).get("temperature") or 0),
                    "max_temp": float(parts.get("max", {}).get("temperature") or 0),
                    "description": parts.get("wx", {}).get("weather", ""),
                }
            )

    return rows


def build_database(rows: List[Dict], db_path: Path = DB_PATH) -> None:
    """Create or refresh the SQLite database with parsed rows."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            date TEXT NOT NULL,
            min_temp REAL,
            max_temp REAL,
            description TEXT,
            UNIQUE(location, date)
        )
        """
    )
    cur.execute("DELETE FROM weather")
    cur.executemany(
        """
        INSERT OR REPLACE INTO weather (location, date, min_temp, max_temp, description)
        VALUES (:location, :date, :min_temp, :max_temp, :description)
        """,
        rows,
    )
    conn.commit()
    conn.close()


def main() -> None:
    rows = parse_weather()
    build_database(rows)
    print(f"Wrote {len(rows)} rows to {DB_PATH}")


if __name__ == "__main__":
    main()
