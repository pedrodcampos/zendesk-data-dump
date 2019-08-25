from .request import ZendeskRequest
from urllib.parse import quote


class ZendeskClient(ZendeskRequest):
    __permission_groups_key__ = 'permission_groups'
    __permission_groups_endpoint__ = 'guide/permission_groups'
    __users_key__ = 'users'
    __users_endpoint__ = 'users'
    __search_endpoint__ = 'search'
    __search_key__ = 'results'
    __ticket_fields_endpoint__ = 'ticket_fields'
    __ticket_fields_key__ = 'ticket_fields'
    __ticket_metrics_endpoint__ = 'tickets/:id/metrics'
    __ticket_metrics_key__ = 'ticket_metric'
    __per_page__ = 1000

    def __init__(self, url, auth):
        super().__init__(url, auth)

    def permission_groups(self):
        return super().__get__(*self.__permission_groups_endpoint__.split('/'), keys=[self.__permission_groups_key__], params=None)

    def users(self):
        return super().__get__(*self.__users_endpoint__.split('/'), keys=[self.__users_key__], params=None)

    def ticket_fields(self):
        return super().__get__(*self.__ticket_fields_endpoint__.split('/'), keys=[self.__ticket_fields_key__], params=None)

    def get_ticket_metrics(self, ticketId):
        url = self.__ticket_metrics_endpoint__.replace(':id', str(ticketId))
        return super().__get__(*url.split('/'), keys=[self.__ticket_metrics_key__], params=None)

    def search(self, query):
        params = {
            'query': query,
            'per_page': self.__per_page__}
        return super().__get__(*self.__search_endpoint__.split("/"), keys=[self.__search_key__], params=params)


class ZendeskHC(ZendeskRequest):
    __articles_endpoint__ = 'articles'
    __articles_key__ = 'articles'
    __categories_endpoint__ = 'categories'
    __categories_key__ = 'categories'
    __sections_endpoint__ = 'sections'
    __sections_key__ = 'sections'
    __user_segments_endpoint__ = 'user_segments'
    __user_segments_key__ = 'user_segments'
    __per_page__ = 1000

    def __init__(self, url, auth):
        super().__init__(url, auth, prefix='hc')

    def __get_per_page_param(self):
        return {'per_page': self.__per_page__}

    def articles(self, include=None):
        params = self.__get_per_page_param()
        keys = [self.__articles_key__]
        if include:
            params.update({'include': include})
            keys = keys+include.split(',')

        return super().__get__(self.__articles_endpoint__, keys=keys, params=params)

    def categories(self):
        params = self.__get_per_page_param()
        return super().__get__(self.__categories_endpoint__, keys=[self.__categories_key__], params=params)

    def sections(self):
        params = self.__get_per_page_param()
        return super().__get__(self.__sections_endpoint__, keys=[self.__sections_key__], params=params)

    def user_segments(self):
        params = self.__get_per_page_param()
        return super().__get__(self.__user_segments_endpoint__, keys=[self.__user_segments_key__], params=params)
