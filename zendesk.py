import requests


class ZendeskHC:
    __articles_endpoint__ = 'articles'
    __articles_key__ = 'articles'
    __categories_endpoint__ = 'categories'
    __categories_key__ = 'categories'
    __sections_endpoint__ = 'sections'
    __sections_key__ = 'sections'

    def __init__(self, url, auth):
        self.__url = url
        self.__requests = requests
        self.__requests.auth.HTTPBasicAuth(*auth)

    def __get_enpoint_url(self, *args):
        return self.__url+'/'.join(map(str, args))

    def __reduce(self, data):
        reduced = {}
        for item in data:
            item_id = item['id']
            reduced.update({item_id: item})
        return [item for item in reduced.values()]

    def __page_response(self, response, keys):
        response = response.json()
        next_url = response.get('next_page', None)
        data = {key: response.get(key) for key in keys}
        while next_url:
            response = self.__requests.get(next_url).json()
            for key in keys:
                data[key] = data[key]+response[key]
                data[key] = self.__reduce(data[key])
            next_url = response.get('next_page', None)

        return data.values()

    def __get(self, keys=None, params=None, *endpoint_parts):
        url = self.__get_enpoint_url(*endpoint_parts)
        response = self.__requests.get(url, params=params)
        return self.__page_response(response, keys)

    def articles(self, include=None):
        if include:
            include = {'include': include}
            keys = [self.__articles_key__]+include['include'].split(',')
        return self.__get(keys, include, self.__articles_endpoint__)

    def categories(self):
        return self.__get(self.__categories_key__, self.__categories_endpoint__)

    def sections(self):
        return self.__get(self.__sections_key__, self.__sections_endpoint__)
