import os
import pickle


class Storage:
    def __init__(self, storage_dir, max_items_in_memory=20):
        if not os.path.exists(storage_dir):
            os.mkdir(storage_dir)
        self.storage_dir = storage_dir
        self.items = {}
        self.max_items_in_memory = max_items_in_memory

    def load_item(self, key):
        with open(os.path.join(self.storage_dir, key), 'rb') as item_file:
            return pickle.load(item_file)

    def dump_item(self, key, item):
        with open(os.path.join(self.storage_dir, key), 'wb') as item_file:
            pickle.dump(item, item_file)

    def is_item_exists_as_file(self, key):
        return key in os.listdir(self.storage_dir)

    def __getitem__(self, key):
        item = self.get(key)
        if item is None:
            raise KeyError("item with key {} doesn't exists".format(key))

    def __setitem__(self, key, item):
        self.dump_item(key, item)
        self.items[key] = item
        self.normalize()

    def get(self, key, default_value=None):
        if key in self.items:
            return self.items[key]
        if self.is_item_exists_as_file(key):
            item = self.load_item(key)
            self.items[key] = item
            self.normalize()
            return item
        return default_value

    def normalize(self):
        if len(self.items) >= self.max_items_in_memory:
            self.items = {}
