from .core import ZendeskClient, ZendeskHC


class Zendesk():
    def __init__(self, instance, helpcenter, auth):
        self.__client = ZendeskClient(instance, auth)
        self.__helpcenter = ZendeskHC(helpcenter, auth)

    @property
    def client(self):
        return self.__client

    @property
    def helpcenter(self):
        return self.__helpcenter
