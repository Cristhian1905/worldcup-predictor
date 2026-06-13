import sqlite3

conn = sqlite3.connect(
    "data/worldcup.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT
    u.name,
    m.home_team,
    m.away_team,
    p.pred_home,
    p.pred_away
FROM predictions p

JOIN users u
ON p.user_id = u.id

JOIN matches m
ON p.match_id = m.id

ORDER BY
    u.name,
    m.match_datetime
""")

for row in cursor.fetchall():

    print(
        f"{row[0]:15} | "
        f"{row[1]} vs {row[2]} | "
        f"{row[3]}-{row[4]}"
    )

conn.close()
