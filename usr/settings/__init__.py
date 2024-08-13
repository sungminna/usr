import os
from .base import *

env = os.environ.get('DJANGO_ENV', 'prod')

if env == 'prod':
    from .prod import *
elif env == 'dev':
    from .dev import *
else:
    raise Exception('Unknown environment')
