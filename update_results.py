import sqlite3
import requests
import streamlit as st

API_KEY = st.secrets[
    "FOOTBALL_API_TOKEN"
]
URL = "https://api.football-data.org/v4/matches"


def update_results():

    headers = {
        "X-Auth-Token": API_KEY
    }

    response = requests.get(
        URL,
        headers=headers
    )

    if response.status_code != 200:

        print(
            "Error API:",
            response.status_code
        )

        return

    data = response.json()

    conn = sqlite3.connect(
        "data/worldcup.db"
    )

    cursor = conn.cursor()

    updated = 0

    for match in data["matches"]:

        if match["status"] != "FINISHED":
            continue

        home_team = (
            match["homeTeam"]["name"]
        )

        away_team = (
            match["awayTeam"]["name"]
        )

        home_score = (
            match["score"]["fullTime"]["home"]
        )

        away_score = (
            match["score"]["fullTime"]["away"]
        )

        cursor.execute(
            """
            UPDATE matches
            SET
                home_score=?,
                away_score=?,
                finished=1
            WHERE
                home_team=?
            AND
                away_team=?
            """,
            (
                home_score,
                away_score,
                home_team,
                away_team
            )
        )

        if cursor.rowcount > 0:

            updated += 1

            print(
                f"Actualizado: "
                f"{home_team} "
                f"{home_score}-{away_score} "
                f"{away_team}"
            )

    conn.commit()
    conn.close()

    print(
        f"\nPartidos actualizados: {updated}"
    )


if __name__ == "__main__":

    update_results()
