from decouple import config


def get_env_vars():
    config_allowed_hosts = config('ALLOWED_HOSTS_PROD')
    if config_allowed_hosts != 'None':
        ALLOWED_HOSTS_PROD = config_allowed_hosts.split(', ')
    else:
        ALLOWED_HOSTS_PROD = []

    return {
        'SECRET_KEY': config('SECRET_KEY_PROD'),
        'DEBUG': True,
        'ALLOWED_HOSTS': ALLOWED_HOSTS_PROD,
        'CORS_ALLOWED_ORIGINS': config('CORS_ALLOWED_ORIGINS_PROD').split(', '),
    }