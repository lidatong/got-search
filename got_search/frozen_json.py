import json


class FrozenJson:
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return FrozenJson(self._data[key])

    def __getattr__(self, name):
        return FrozenJson(self._data[name])

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        # if isinstance(self.data, list)
        return json.dumps(self._data, sort_keys=True, indent=4)

    def get(self):
        return self._data

    @staticmethod
    def loads(json_s):
        return FrozenJson(json.loads(json_s))
