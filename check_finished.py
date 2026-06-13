import sqlite3

conn = sqlite3.connect(
    "data/worldcup.db"
)

cursor = conn.cursor()

cursor.execute(
    """
    SELECT
        home_team,
        away_team,
        home_score,
        away_score,
        finished
    FROM matches
    WHERE finished = 1
    """
)

for row in cursor.fetchall():

    print(row)

conn.close()
