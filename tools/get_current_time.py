"""Return current time tool."""
from datetime import datetime, timezone


def now(utc: bool = True):
    dt = datetime.now(timezone.utc if utc else None)
    return {"iso": dt.isoformat(), "utc": utc}


if __name__ == "__main__":
    print(now())
