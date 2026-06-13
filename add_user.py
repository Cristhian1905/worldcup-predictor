import sqlite3
from werkzeug.security import generate_password_hash

name = input("Nombre: ")
username = input("Usuario: ")
password = input("Contraseña: ")

hashed = generate_password_hash(password)

conn = sqlite3.connect(
    "data/worldcup.db"
)

cursor = conn.cursor()

cursor.execute(
    """
    INSERT INTO users
    (
        name,
        username,
        password,
        role
    )
    VALUES
    (
        ?,?,?,?
    )
    """,
    (
        name,
        username,
        hashed,
        "user"
    )
)

conn.commit()
conn.close()

print("Usuario creado")
