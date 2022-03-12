"""
caches
"""

from xml.dom import NotSupportedErr
import boto3
import json
import pickle
import time


class RedisCache(object):
    """Redis cache"""

    # From http://blog.seevl.fm/2013/11/22/simple-caching-with-redis/

    def __init__(self, redis, prefix='cache|', timeout=60*60):
        """Create Redis cache instance using a StrictRedis connection,
        with prefix and timeout (or use default one)"""
        assert redis
        self._redis = redis
        self._prefix = prefix
        self._timeout = timeout

    def set(self, key, value, timeout=None):
        """Set key-value in cache with given timeout (or use default one)"""
        timeout = timeout or self._timeout
        key = self._prefix + key
        # Add key and define an expire timeout in a pipeline for atomicity
        self._redis.pipeline().set(key, pickle.dumps(value)).expire(key, timeout).execute()

    def get(self, key):
        """Get key-value from cache"""
        data = self._redis.get(self._prefix + key)
        return (data and pickle.loads(data)) or None

    def flush(self, pattern='', step=1000):
        """Flush all cache (by group of step keys for efficiency),
        or only keys matching an optional pattern"""
        keys = self._redis.keys(self._prefix + pattern + '*')
        [self._redis.delete(*keys[i:i+step]) for i in range(0, len(keys), step)]


class DynamoCache:
    """AWS DynamoDB cache"""
    

    def __init__(self, table_name, prefix='cache|', timeout=60*60):
        """Create DynamoDB cache instance"""
        assert table_name
        self._table = boto3.resource('dynamodb').Table(table_name)
        self._prefix = prefix
        self._timeout = timeout


    def set(self, key, value, timeout=None):
        """Set key-value in cache with given timeout (or use default one)"""
        timeout = timeout or self._timeout
        key = self._prefix + key
        print(key)
        self._table.put_item(
            Item={
                'key': key,
                'value': json.dumps(value),
                'expires': int(time.time()) + timeout
            }
        )
        

    def get(self, key):
        """Get key-value from cache"""
        data = self._table.get_item(Key={ 'key': self._prefix + key })
        print(data)
        if data:
            item = data['Item']
            expires = item['expires']
            print(expires)
            if expires > time.time(): # type: ignore
                print(item['value'])
                value = item['value']
                if isinstance(value, str):
                    return json.loads(value)
        return None
        

    def flush(self, pattern='', step=1000):
        raise NotSupportedErr()

        