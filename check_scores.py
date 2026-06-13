import sqlite3

conn = sqlite3.connect(
    "data/worldcup.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT
id,
user_id,
match_id,
points
FROM scores
ORDER BY id
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
