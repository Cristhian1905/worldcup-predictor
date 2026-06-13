import sqlite3

conn = sqlite3.connect(
    "data/worldcup.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT sql
FROM sqlite_master
WHERE type='table'
AND name='predictions'
""")

print(cursor.fetchone()[0])

conn.close()
