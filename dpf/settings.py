import os
import sys

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.realpath(os.path.join(root, os.pardir)))

from dpf.conf.default import *


#
# Load settings based on deployment context
#

ENVIRON = os.environ.get('DEPLOYMENT_CONTEXT', 'development')

# load custom settings
custom_settings = __import__('dpf.conf.' + ENVIRON,
                             locals(), globals(), ['*'])
for key in dir(custom_settings):
    if not key.startswith('_'):
        locals()[key] = getattr(custom_settings, key)

#
# Load local settings
#

try:
    from local_settings import *
except ImportError, exc:
    sys.stderr.write("Skipping local_settings import (from %r): %s\n" %
                     (__file__, exc))


