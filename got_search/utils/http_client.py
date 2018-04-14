import requests
from got_search.utils.frozen_json import FrozenJson
from got_search.utils.functools2 import delay


class HttpClient:
    def __init__(self,
                 base_url,
                 base_route=None):
        self.base_url = (base_url if base_route is None
                         else f'{base_url}/{base_route}')

    @delay()
    def get(self, route) -> str:
        r = requests.get(f'{self.base_url}/{route}')
        return r.text

    @delay()
    def get_json(self, route) -> FrozenJson:
        r = requests.get(f'{self.base_url}/{route}')
        return FrozenJson(r.json())
