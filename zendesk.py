import requests


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
            print(f"Getting page {response['page']}/{response['page_count']}")
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


class ZendeskClient(ZendeskRequest):
    __permission_groups_key__ = 'permission_groups'
    __permission_groups_endpoint__ = 'guide/permission_groups'

    def __init__(self, url, auth):
        super().__init__(url, auth)

    def permission_groups(self):
        return super().__get__(*self.__permission_groups_endpoint__.split('/'), keys=[self.__permission_groups_key__], params=None)


class ZendeskHC(ZendeskRequest):
    __articles_endpoint__ = 'articles'
    __articles_key__ = 'articles'
    __categories_endpoint__ = 'categories'
    __categories_key__ = 'categories'
    __sections_endpoint__ = 'sections'
    __sections_key__ = 'sections'
    __user_segments_endpoint__ = 'user_segments'
    __user_segments_key__ = 'user_segments'

    def __init__(self, url, auth):
        super().__init__(url, auth, prefix='hc')

    def articles(self, include=None):
        params = {'per_page': 1000}
        keys = [self.__articles_key__]
        if include:
            params.update({'include': include})
            keys = keys+include.split(',')

        return super().__get__(self.__articles_endpoint__, keys=keys, params=params)

    def categories(self):
        params = {'per_page': 1000}
        return super().__get__(self.__categories_endpoint__, keys=[self.__categories_key__], params=params)

    def sections(self):
        params = {'per_page': 1000}
        return super().__get__(self.__sections_endpoint__, keys=[self.__sections_key__], params=params)

    def user_segments(self):
        params = {'per_page': 1000}
        return super().__get__(self.__user_segments_endpoint__, keys=[self.__user_segments_key__], params=params)
