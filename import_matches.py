import sqlite3
import pandas as pd


def import_matches(csv_file):

    conn = sqlite3.connect(
        "data/worldcup.db"
    )

    cursor = conn.cursor()

    df = pd.read_csv(csv_file)

    imported = 0

    for _, row in df.iterrows():

        cursor.execute("""
        INSERT INTO matches
        (
            home_team,
            away_team,
            match_datetime,
            stage
        )
        VALUES(?,?,?,?)
        """,
        (
            row["home_team"],
            row["away_team"],
            row["match_datetime"],
            row["stage"]
        ))

        imported += 1

    conn.commit()
    conn.close()

    return imported
