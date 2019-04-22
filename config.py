from os import path


def load_env():
    env = {}
    filename = path.join(path.curdir, '.env')
    with open(filename) as envfile:
        for line in envfile:
            key, value = line.split("=")
            env.update({key: value})
    return env


def build_zendesk_config(instance=None, helpcenter=None, username=None, password=None):
    environ = load_env()
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
