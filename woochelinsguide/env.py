from decouple import config


def get_env_vars():
    config_allowed_hosts = config('ALLOWED_HOSTS_DEV')
    if config_allowed_hosts != 'None':
        ALLOWED_HOSTS_DEV = config_allowed_hosts.split(', ')
    else:
        ALLOWED_HOSTS_DEV = []

    return {
        'SECRET_KEY': config('SECRET_KEY_DEV'),
        'DEBUG': True,
        'ALLOWED_HOSTS': ALLOWED_HOSTS_DEV,
        'CORS_ALLOWED_ORIGINS': config('CORS_ALLOWED_ORIGINS_DEV').split(', '),
    }