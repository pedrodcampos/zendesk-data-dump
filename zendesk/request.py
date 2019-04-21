import requests
from urllib.parse import urlparse, parse_qs


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
        next_url = response.get('next_page', None)
        data = {key: response.get(key) for key in keys}
        while next_url:
            query = parse_qs(urlparse(next_url).query)
            page = query.get('page')
            response = self.__session.get(next_url, params=params).json()
            for key in keys:
                if key in response:
                    data[key] = data[key]+response[key]
                    data[key] = self.__reduce(data[key])
            next_url = response.get('next_page', None)

        return data.values()

    def __get__(self, *endpoint_parts, keys=None,  params=None):
        url = self.__get_enpoint_url(*endpoint_parts)
        response = self.__session.get(url, params=params)
        if response.status_code == 200:
            return self.__page_response(response, keys, params)
        else:
            raise BaseException(f"Zendesk API Error:{response.status_code}")
