from os import environ


def build_zendesk_config(instance=None, helpcenter=None, username=None, password=None):

    return {
        'instance': instance if instance else environ.get('INSTANCE', None),
        'helpcenter': helpcenter if helpcenter else environ.get('HELPCENTER', None),
        'auth': (
            username
            if username else environ.get('USERNAME', None),
            password
            if password else environ.get('PASSWORD', None)
        )
    }
