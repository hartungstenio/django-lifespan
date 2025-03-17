# django-lifespan

[![PyPI - Version](https://img.shields.io/pypi/v/django-lifespan.svg)](https://pypi.org/project/django-lifespan)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-lifespan.svg)](https://pypi.org/project/django-lifespan)

`django-lifespan` adds support for [ASGI Lifespan Protocol](https://asgi.readthedocs.io/en/latest/specs/lifespan.html) to your [Django](https://www.djangoproject.com/) project. Currently depends on [Django Channels](https://channels.readthedocs.io/en/latest/).

## Dependencies
* Python 3.9 and up
* Django 4.2, 5.0 and 5.1

## Installation

```console
pip install django-lifespan
```

## Quickstart

### Integrate with Channels
Django only supports HTTP events. Luckly, `channels` provide a routing configuration to support other events:

```python
# mysite/asgi.py
import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from django_lifespan import LifespanConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter(
    {
        "lifespan": LifespanConsumer.as_asgi(),
        "http": get_asgi_application(),
    }
)
```

## License

`django-lifespan` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
