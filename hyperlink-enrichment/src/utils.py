
from collections.abc import Sized
from datetime import datetime, timedelta, timezone, tzinfo


class TimeUtil:
    # import zoneinfo
    # ZONE_ASIA_SHANGHAI = zoneinfo.ZoneInfo("Asia/Shanghai")
    ASIA_SHANGHAI = timezone(timedelta(hours=8), 'Asia/Shanghai')

    @classmethod
    def atstartday(cls, dt: datetime, tz:tzinfo = None) -> datetime:
        # return a new object.
        return dt.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tz)

    @classmethod
    def fromtimestamp(cls, epochseconds: int, tz: tzinfo = None) -> datetime:
        return datetime.fromtimestamp(int(epochseconds), tz)

    @classmethod
    def fromstring(cls, date_string: str, fmt: str = None) -> datetime:
        return (
            datetime.strptime(date_string, fmt)
            if fmt
            else datetime.fromisoformat(date_string)
        )

    @classmethod
    def toepochseconds(cls, dt: datetime, tz: tzinfo = None) -> int:
        # datetime.timestamp() converts this datetime object to a Unix timestamp in seconds since the epoch.
        # int() converts the floating-point timestamp to an integer, if needed.
        return int(dt.astimezone(tz).timestamp() if tz else dt.timestamp())

    @classmethod
    def str2epochseconds(
        cls, date_string: str, fmt: str = None, tz: tzinfo = None
    ) -> int:
        return cls.toepochseconds(cls.fromstring(date_string, fmt), tz)

    @classmethod
    def isafter(cls, epoch_seconds: int, date: datetime) -> bool:
        return epoch_seconds > cls.toepochseconds(date)


class StrUtil:
    @classmethod
    def isblank(cls, s: str) -> bool:
        return not s or s.isspace()


class IterUtil:
    @classmethod
    def isempty(cls, iter: Sized) -> bool:
        return not iter or len(iter) == 0


def is_after(epoch_seconds: int, date_string: str) -> bool:
    if not epoch_seconds or StrUtil.isblank(date_string):
        return False
    return epoch_seconds > TimeUtil.str2epochseconds(
        date_string, "%Y-%m-%d", TimeUtil.ASIA_SHANGHAI
    )
