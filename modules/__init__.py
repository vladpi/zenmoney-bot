import inspect
import sys

from .bot import *  # noqa
from .users import *  # noqa

routers = []
for _, module in inspect.getmembers(sys.modules[__name__], inspect.ismodule):
    if router := module.__dict__.get('router'):
        routers.append(router)
