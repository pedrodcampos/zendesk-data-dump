import requests


class ZendeskHC:
    __articles_endpoint__ = 'articles'
    __articles_key__ = 'articles'

    def __init__(self, url, auth):
        self.__url = url
        self.__requests = requests
        self.__requests.auth.HTTPBasicAuth(*auth)

    def __get_enpoint_url(self, *args):
        return self.__url+'/'.join(map(str, args))

    def __page_response(self, response, key):
        response = response.json()
        next_url = response.get('next_page', None)
        data = response[key]
        while next_url:
            response = self.__requests.get(next_url).json()
            data = data + response[key]
            next_url = response.get('next_page', None)

        return data

    def articles(self):
        url = self.__get_enpoint_url(self.__articles_endpoint__)
        response = self.__requests.get(url)
        return self.__page_response(response, self.__articles_key__)
