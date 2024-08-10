from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def is_after(epoch_seconds: str | int, date_str: str):
    if not date_str or date_str.isspace() or not epoch_seconds:
        return False
    datetime.fromtimestamp(int(epoch_seconds), timezone(timedelta(hours=8), 'Asia/Shanghai') )
    datetime.fromtimestamp(int(epoch_seconds), ZoneInfo("Asia/Shanghai"))
    date.fromtimestamp(epoch_seconds)
