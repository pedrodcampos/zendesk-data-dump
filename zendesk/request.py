import requests
import time
from urllib.parse import urlparse, parse_qs, urlencode


class ZendeskRequest:
    def __init__(self, url, auth, prefix=None):
        self.__url = url
        self.__session = requests.Session()
        self.__session.auth = auth
        self.__version = 'v2'
        self.__prefix = prefix

    def __get_enpoint_url(self, *args):
        path = []
        if self.__prefix:
            path.append(self.__prefix)
        path = path+['api', self.__version]+list(args)
        path = "/".join(map(str, path))
        return f"{self.__url}{path}"

    def __reduce(self, data):
        reduced = {}
        for item in data:
            item_id = item['id']
            reduced.update({item_id: item})
        return [item for item in reduced.values()]

    def __page_response(self, response, keys, params):
        response = response.json()
        data = {key: response.get(key) for key in keys}
        next_url = response.get('next_page', None)
        while next_url:
            count = response.get('count', None)
            print(f'Got {len(data[keys[0]])}/{count}')

            response = self.__session.get(next_url).json()
            for key in keys:
                if key in response:
                    data[key] = data[key]+response[key]
            next_url = response.get('next_page', None)

        return data.values()

    def __get__(self, *endpoint_parts, keys=None,  params=None):
        data = {}
        url = self.__get_enpoint_url(
            *endpoint_parts)+('?'+urlencode(params) if params else "")

        while url:
            response = self.__session.get(url)

            if response.status_code == 429:
                print('Rate limited! Please wait.')
                time.sleep(int(response.headers['retry-after']))
                continue

            if response.status_code == 502:
                print('Server error; Retrying in 5 sec.')
                time.sleep(5)
                continue

            if response.status_code != 200:
                raise BaseException(
                    f"Zendesk API Error:{response.status_code}")

            response = response.json()

            for key in keys:
                if key in data:
                    data[key].extend(response.get(key, None))
                else:
                    data[key] = response.get(key, None)

            count = response.get('count', None)
            url = response.get('next_page', None)
            if count is not None:
                print(f'Got {len(data[keys[0]])}/{count}')

        for key in keys:
            if key in data:
                if type(data[key]) == list:
                    data[key] = self.__reduce(data[key])

        return data.values()
