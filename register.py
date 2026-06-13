import sqlite3
import bcrypt

def register_user(
    name,
    username,
    password
):

    conn = sqlite3.connect(
        "data/worldcup.db"
    )

    cursor = conn.cursor()

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:

        cursor.execute("""
        INSERT INTO users
        (
            name,
            username,
            password,
            role
        )
        VALUES(?,?,?,?)
        """,
        (
            name,
            username,
            hashed,
            "user"
        ))

        conn.commit()

        return True

    except Exception:

        return False

    finally:

        conn.close()
