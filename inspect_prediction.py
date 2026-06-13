import sqlite3

conn = sqlite3.connect(
    "data/worldcup.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT
user_id,
match_id,
pred_home,
pred_away
FROM predictions
WHERE match_id = 76
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
