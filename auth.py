import sqlite3
import bcrypt
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)



def login(username, password):

    conn = sqlite3.connect("data/worldcup.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, password, role
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    if user:

        stored_password = user[2]

        # SQLite puede devolver str o bytes
        if isinstance(stored_password, str):
            stored_password = stored_password.encode()

        if bcrypt.checkpw(
            password.encode(),
            stored_password
        ):
            return {
                "id": user[0],
                "name": user[1],
                "role": user[3]
            }

    return None
