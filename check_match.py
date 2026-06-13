import sqlite3

conn = sqlite3.connect(
    "data/worldcup.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT
id,
home_team,
away_team,
home_score,
away_score,
finished
FROM matches
WHERE id = 76
""")

print(
    cursor.fetchone()
)

conn.close()
