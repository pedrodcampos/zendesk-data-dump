from os import environ
ZENDESK_HELPCENTER_INSTANCE = environ.get('ZENDESK_HELPCENTER_INSTANCE', None)
ZENDESK_INSTANCE = environ.get('ZENDESK_INSTANCE', None)
AUTH = (environ.get('USER', None), environ.get('PASSWORD', None))
