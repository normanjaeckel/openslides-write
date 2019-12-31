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
        Acquire lock for the given key. Use this with a context manager. The
        lock expires after worker timeout. We add one extra second to ensure
        that - after a SIGTERM from the master process the context manager exits
        cleanly before the lock expires.
        """
        expire = int(os.environ.get("OPENSLIDES_WRITE_SERVICE_WORKER_TIMEOUT", 30)) + 1
        return redis_lock.Lock(self.connection, key, expire=expire)
