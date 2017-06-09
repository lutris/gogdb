import redis

REDIS_HOSTNAME = 'localhost'
REDIS_PORT = 6379
REDIS_URL = 'redis://{}:{}/0'.format(REDIS_HOSTNAME, REDIS_PORT)
REDIS = redis.StrictRedis(host=REDIS_HOSTNAME, port=REDIS_PORT)

GOGDB_NS = "gogdb:"
