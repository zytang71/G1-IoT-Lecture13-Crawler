import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).parent / "data.db"


@st.cache_data
def load_data() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        """
        SELECT location, date, min_temp, max_temp, description
        FROM weather
        ORDER BY date, location
        """,
        conn,
    )
    conn.close()
    return df


def main() -> None:
    st.set_page_config(page_title="CWA Weather Crawler", layout="wide")
    st.title("氣象署農業氣象一週預報")
    st.caption("資料來源：中央氣象署 F-A0010-001")

    df = load_data()

    locations = ["全部"] + sorted(df["location"].unique().tolist())
    picked = st.selectbox("選擇地區", locations)
    filtered = df if picked == "全部" else df[df["location"] == picked]

    st.dataframe(filtered, use_container_width=True)

    st.metric("資料筆數", len(filtered))


if __name__ == "__main__":
    main()
