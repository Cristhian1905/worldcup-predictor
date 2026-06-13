import sqlite3

conn = sqlite3.connect(
    "data/worldcup.db"
)

cursor = conn.cursor()

cursor.execute("""
UPDATE matches
SET
    home_score = 2,
    away_score = 1,
    finished = 1
WHERE id = 76
""")

conn.commit()
conn.close()

print(
    "Resultado de prueba cargado"
)
