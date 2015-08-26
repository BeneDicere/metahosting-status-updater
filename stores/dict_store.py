from copy import copy


class Store(object):
    def __init__(self, *args, **kwargs):
        self.store = dict()

    def update_config(self, values):
        pass

    def update(self, name, value):
        self.store[name] = copy(value)

    def get(self, name):
        if name not in self.store:
            return None
        return copy(self.store[name])

    def get_all(self):
        return copy(self.store)

    def remove(self, name):
        if name in self.store:
            self.store.pop(name)
