import os

import redis
import redis_lock


class Locker:
    """
    Adapter to connect to Redis to access to global lock.
    """

    def __init__(self, connection: redis.Redis) -> None:
        self.connection = connection

    def acquire(self, key: str) -> redis_lock.Lock:
        """
        """
        expire = int(os.environ.get("OPENSLIDES_WRITE_SERVICE_WORKER_TIMEOUT", 30))
        return redis_lock.Lock(self.connection, key, expire=expire, auto_renewal=True)
