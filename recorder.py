
import json
from datetime import datetime, timezone
from pathlib import Path


RECORDS_DIR = Path("runs")


def save_run(data):
    RECORDS_DIR.mkdir(exist_ok=True)

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data
    }

    filename = RECORDS_DIR / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"

    with filename.open("w", encoding="utf-8") as file:
        json.dump(record, file, indent=2)

    return str(filename)
