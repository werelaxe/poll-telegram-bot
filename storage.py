import pickle
import redis


class Storage:
    def __init__(self):
        self.client = redis.StrictRedis()

    def __getitem__(self, key):
        item = self.get(key)
        if item is None:
            raise KeyError("item with key {} doesn't exists".format(key))
        return item

    def __setitem__(self, key, item):
        self.client.set(pickle.dumps(key), pickle.dumps(item), 86400)

    def get(self, key, default_value=None):
        value = self.client.get(pickle.dumps(key))
        if value is None:
            return default_value
        return pickle.loads(value)

    def delete(self, key):
        self.client.delete(pickle.dumps(key))
