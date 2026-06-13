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
WHERE home_team='Mexico'
""")

print("PARTIDO")
print(cursor.fetchone())

print("\nPRONOSTICOS")

cursor.execute("""
SELECT
    p.user_id,
    u.name,
    p.pred_home,
    p.pred_away
FROM predictions p
JOIN users u
ON p.user_id=u.id
WHERE p.match_id=76
""")

for row in cursor.fetchall():
    print(row)

print("\nPUNTOS")

cursor.execute("""
SELECT
    user_id,
    match_id,
    points
FROM scores
WHERE match_id=76
""")

for row in cursor.fetchall():
    print(row)

conn.close()
