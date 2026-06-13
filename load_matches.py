import sqlite3

conn = sqlite3.connect("data/worldcup.db")

cursor = conn.cursor()

matches = [

(
"Mexico",
"Canada",
"2026-06-11 20:00",
"Grupo A"
),

(
"USA",
"Colombia",
"2026-06-12 18:00",
"Grupo A"
),

(
"España",
"Brasil",
"2026-06-13 19:00",
"Grupo B"
)

]

for match in matches:

    cursor.execute("""
    INSERT INTO matches(
        home_team,
        away_team,
        match_datetime,
        stage
    )
    VALUES(?,?,?,?)
    """, match)

conn.commit()
conn.close()

print("Partidos cargados")
