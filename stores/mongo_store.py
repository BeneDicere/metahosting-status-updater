from pymongo import MongoClient
from retrying import retry
from stores.abstract_kv_store import AbstractKVStore


class MongoStore(AbstractKVStore):
    def initialize_collection(self):
        url = 'mongodb://{}:{}/{}'.format(
            self.get_property('host'),
            self.get_property('port'),
            self.get_property('database'))
        return self._initialize_connection(url)

    @retry(stop_max_attempt_number=10, wait_fixed=1000)
    def _initialize_connection(self, url):
        client = MongoClient(host=url)
        return client[
            self.get_property('database')][self.get_property('collection')]

    def update(self, name, value):
        self.collection.update(spec={'name': name},
                               document={'name': name, 'value': value},
                               upsert=True)

    def insert(self, item):
        self.collection.insert_one(item)
