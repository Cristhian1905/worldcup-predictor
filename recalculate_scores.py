import sqlite3

from scoring import calculate_points


def recalculate_scores():

    conn = sqlite3.connect(
        "data/worldcup.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM scores"
    )

    cursor.execute(
        """
        SELECT

        p.user_id,
        p.match_id,

        p.pred_home,
        p.pred_away,

        m.home_score,
        m.away_score

        FROM predictions p

        JOIN matches m
        ON p.match_id = m.id

        WHERE m.finished = 1
        """
    )

    rows = cursor.fetchall()

    for row in rows:

        user_id = row[0]
        match_id = row[1]

        pred_home = row[2]
        pred_away = row[3]

        real_home = row[4]
        real_away = row[5]

        points = calculate_points(
            pred_home,
            pred_away,
            real_home,
            real_away
        )

        cursor.execute(
            """
            INSERT INTO scores
            (
                user_id,
                match_id,
                points
            )
            VALUES
            (
                ?,?,?
            )
            """,
            (
                user_id,
                match_id,
                points
            )
        )

    conn.commit()
    conn.close()

    print(
        "Clasificación recalculada"
    )
