from datetime import datetime
import os

FILE = "data/last_update.txt"


def should_update(minutes=15):

    if not os.path.exists(FILE):
        return True

    with open(FILE, "r") as f:

        value = f.read().strip()

    if not value:
        return True

    last = datetime.fromisoformat(value)

    diff = datetime.now() - last

    return diff.total_seconds() > minutes * 60


def mark_updated():

    with open(FILE, "w") as f:

        f.write(
            datetime.now().isoformat()
        )
