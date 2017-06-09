import json
import redis
from gogdb import settings


class GOGStore:
    def __init__(self):
        self.store = redis.StrictRedis(host=settings.REDIS_HOSTNAME,
                                       port=settings.REDIS_PORT)

    def set(self, key, value):
        self.store.set(settings.GOGDB_NS + key, value)

    def get(self, key):
        return self.store.get(settings.GOGDB_NS + key)

    def keys(self, pattern):
        return self.store.keys(settings.GOGDB_NS + pattern)

    def set_page(self, page, value):
        self.set("page:%d" % page, json.dumps(value))

    def get_page(self, page):
        return json.loads(self.get("page:%d" % page))

    def get_page_count(self):
        return len(self.keys("page:*"))
