from os import environ
ZENDESK_HC_API_URL = f"{environ.get('ZENDESK_HELPCENTER_INSTANCE', None)}api/v2/"
AUTH = (environ.get('USER', None), environ.get('PASSWORD', None))
