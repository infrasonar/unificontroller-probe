import time


class ConnectionCache:
    _all = {}

    @classmethod
    def get_value(cls, key):
        if key in cls._all:
            val, expire_ts = cls._all[key]
            expired = expire_ts and expire_ts < time.time()
            if expired:
                del cls._all[key]
            else:
                return val
        return None

    @classmethod
    def set_value(cls, key, val, max_age=None):
        expire_ts = time.time() + max_age if max_age else None
        cls._all[key] = (val, expire_ts)
