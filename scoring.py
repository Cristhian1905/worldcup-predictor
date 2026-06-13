import sqlite3


def save_prediction(
    user_id,
    match_id,
    pred_home,
    pred_away
):

    conn = sqlite3.connect(
        "data/worldcup.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO predictions
        (
            user_id,
            match_id,
            pred_home,
            pred_away,
            created_at
        )
        VALUES
        (
            ?,?,?,?,
            datetime('now')
        )
        """,
        (
            user_id,
            match_id,
            pred_home,
            pred_away
        )
    )

    conn.commit()
    conn.close()


def get_prediction(
    user_id,
    match_id
):

    conn = sqlite3.connect(
        "data/worldcup.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            pred_home,
            pred_away
        FROM predictions
        WHERE user_id=?
        AND match_id=?
        """,
        (
            user_id,
            match_id
        )
    )

    row = cursor.fetchone()

    conn.close()

    return row


# --------------------------------
# SISTEMA DE PUNTOS
# --------------------------------

def calculate_points(
    pred_home,
    pred_away,
    real_home,
    real_away
):

    points = 0

    predicted_result = 0
    real_result = 0

    # Resultado pronosticado

    if pred_home > pred_away:
        predicted_result = 1

    elif pred_home < pred_away:
        predicted_result = -1

    # Resultado real

    if real_home > real_away:
        real_result = 1

    elif real_home < real_away:
        real_result = -1

    # Acertó ganador o empate

    if predicted_result == real_result:

        if real_result == 0:

            # Acertó empate
            points += 1

        else:

            # Acertó ganador
            points += 3

    # Marcador exacto

    if (
        pred_home == real_home
        and
        pred_away == real_away
    ):

        points += 3

    return points
# --------------------------------
# CONSULTAR PUNTOS
# --------------------------------

def get_points_for_prediction(
    user_id,
    match_id
):

    conn = sqlite3.connect(
        "data/worldcup.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT points
        FROM scores
        WHERE user_id=?
        AND match_id=?
        """,
        (
            user_id,
            match_id
        )
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        return row[0]

    return 0
