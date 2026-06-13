import sqlite3
import bcrypt

conn = sqlite3.connect("data/worldcup.db")

cursor = conn.cursor()

username = "admin"
password = "1234"

hashed = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
)

cursor.execute("""
INSERT OR IGNORE INTO users
(name,username,password,role)
VALUES(?,?,?,?)
""",
(
    "Administrador",
    username,
    hashed,
    "admin"
))

conn.commit()
conn.close()

print("Administrador creado correctamente")
