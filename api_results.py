import sqlite3

from datetime import datetime
from datetime import timedelta


def get_last_update():

    conn = sqlite3.connect(
        "data/worldcup.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT value
        FROM settings
        WHERE key='last_update'
        """
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        return row[0]

    return None


def save_last_update():

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    conn = sqlite3.connect(
        "data/worldcup.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO settings
        (key,value)
        VALUES
        ('last_update',?)
        """,
        (now,)
    )

    conn.commit()
    conn.close()


def should_update():

    last_update = get_last_update()

    if last_update is None:

        return True

    last_update = datetime.strptime(
        last_update,
        "%Y-%m-%d %H:%M:%S"
    )

    elapsed = (
        datetime.now() -
        last_update
    )

    if elapsed > timedelta(minutes=15):

        return True

    return False
