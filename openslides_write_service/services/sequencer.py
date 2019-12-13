from typing import Dict

import redis


class Sequencer:
    """
    Adapter to connect to redis sequencer.
    """

    def __init__(self, redis_sequencer_connection: redis.Redis) -> None:
        self.redis_connection = redis_sequencer_connection
        self.headers = {"Content-Type": "application/json"}

    def get(self, keys: Dict[str, int]) -> Dict[str, range]:
        """
        Fetches one or more new ids for every given key from the redis
        sequencer. The value of each key in the keys dictionary is a number of
        how many ids are requested.
        """
        result = {}
        for key, value in keys.items():
            if value <= 0:
                raise ValueError(f"Amount for key {key} must not be smaller than 1.")
            last_key = self.redis_connection.incr(key, amount=value)
            result[key] = range(last_key - value + 1, last_key + 1)
        return result


# Lock setzen, wenn Username schon belegt ist. SET key value EX 600 NX
# set(name, value, ex=None, px=None, nx=False, xx=False)[source]
