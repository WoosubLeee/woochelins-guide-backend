# 개발 기록

## 환경변수 분리하기

개발 - 배포 간 `SECRET_KEY`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`와 같은 환경변수를 분리해보려고 합니다. Django에서 환경변수를 분리하는 법에 대해 검색해본 결과, 다음 글 ([Django: How to manage development and production settings?](https://stackoverflow.com/questions/10664244/django-how-to-manage-development-and-production-settings))에 방법이 많이 나와있었는데 대부분 요지는:

1. `settings.py` 를 `settings_dev.py`, `settings_prod.py`와 같이 분리하여 만들고,
2. `DJANGO_SETTINGS_MODULE`에 상황에 따라 다른 setting을 읽어오라는 것이었습니다.

하지만 어떤 setting을 읽어올지 결정하려면 현재가 개발 환경인지 배포 환경인지 알아야 하는데, 방법으로는 대부분 OS 환경변수에 관련 변수를 추가하는 방식을 이용했습니다. 예를 들어 'woochelinguide'라는 키에 'dev' 혹은 'prod'와 같은 값을 설정하는 것입니다.

### `env.py`

하지만 저는 이 방법을 이용하지 않고, `env.py`라는 모듈을 하나 더 만들어서 branch 별로(master(dev), deployment 각각) 다르게 코드를 작성하여 환경 변수를 바꾸도록 하였습니다. `.env` 파일에 다음과 같이 환경변수를 작성합니다.

```
SECRET_KEY_DEV=django-insecure-l57q1y58i=vg^tw6dv-=3jd6gu(axji%&3lxv19^&=+gm-uv8v
ALLOWED_HOSTS_DEV=None
CORS_ALLOWED_ORIGINS_DEV=http://localhost:3000

SECRET_KEY_PROD=django-insecure-**********************************************
ALLOWED_HOSTS_PROD=woosubleee.pythonanywhere.com
CORS_ALLOWED_ORIGINS_PROD=https://woochelinsguide.com, https://www.woochelinsguide.com
```

그리고 `env.py`에서 이 변수를 읽어 옵니다. 이때 master 브랜치와 deployment 브랜치의 코드를 환경에 맞게 서로 다르게 작성합니다.

````python
# env.py

# dev (master)

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

# prod (deployment)

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
````

`settings.py`에서는 `get_env_vars()` 함수를 읽어와 값을 설정해줍니다.

```python
# settings.py

from woochelinsguide.env import get_env_vars

ENV_VARS = get_env_vars()

SECRET_KEY = ENV_VARS['SECRET_KEY']
DEBUG = ENV_VARS['DEBUG']
ALLOWED_HOSTS = ENV_VARS['ALLOWED_HOSTS']
CORS_ALLOWED_ORIGINS = ENV_VARS['CORS_ALLOWED_ORIGINS']
```

위와 같은 방법으로 환경변수를 분리할 경우 장점은 다음과 같습니다:

1. 프로젝트 내에서 해결할 수 있다 - 프로젝트 외부의 것(e.g. 운영체제)를 조작하지 않아도 된다.
2. 단일 `settings.py`로 환경변수 분리가 가능하다.