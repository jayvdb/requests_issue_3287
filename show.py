from __future__ import print_function

import os.path
import sys

try:
    import urllib3 as urllib3_package
except ImportError as e:
    urllib3_package = e

# Save a copy of the urllib packages before importing requests
urllib3_modules = dict(
    (name, mod)
    for name, mod in sys.modules.items()
    if name.startswith('urllib3')
)

# Import requests' urllib3 first
try:
    from requests.packages import urllib3 as urllib3_bundle
except ImportError as e:
    urllib3_bundle = e
try:
    import requests
except ImportError as e:
    requests = e

print('Packages:')

print('  urllib3: {0}'.format(
    urllib3_package if isinstance(urllib3_package, Exception) else
    os.path.dirname(urllib3_package.__file__)))
print('  requests: {0}'.format(
    requests if isinstance(requests, Exception) else
    os.path.dirname(requests.__file__)))
print('\n')

urllib3_unbundled = (urllib3_package == urllib3_bundle)

if not urllib3_unbundled:
    print('Not unbundled\n')

requests_urllib3_modules = dict(
    (name[len('requests.packages.'):], mod)
    for name, mod in sys.modules.items()
    if name.startswith('requests.packages.urllib3')
)

all_mod_names = set(urllib3_modules.keys()) | set(requests_urllib3_modules.keys())
all_mod_names = sorted(all_mod_names)


def _mod_eq(mod1, mod2):
    id_equal = id(mod1) == id(mod2)
    is_ = mod1 is mod2
    assert id_equal is is_
    return id_equal


def _mod_file(mod):
    try:
        return mod.__file__
    except AttributeError:
        return '{0} ({1}) doesnt have __file__'.format(mod.__name__, id(mod))


for name in all_mod_names:
    if name not in urllib3_modules:
        print('{0}: not loaded in urllib3'.format(name))
    elif name not in requests_urllib3_modules:
        print('{0}: not loaded in requests'.format(name))
    elif not urllib3_unbundled:
        print('{0}: loaded in urllib3 and requests'.format(name))
    elif _mod_eq(urllib3_modules[name], requests_urllib3_modules[name]):
        print('{0}: ok'.format(name))
    elif urllib3_modules[name] == requests_urllib3_modules[name]:
        print('{0}: not ok (equals, but not is)'.format(name))
    elif _mod_file(urllib3_modules[name]) == _mod_file(requests_urllib3_modules[name]):
        print('{0}: not ok (__file__ matches {1})'.format(name, urllib3_modules[name].__file__))
    else:
        print('{0}: {1} vs {2}'.format(name,
                                       urllib3_modules[name],
                                       requests_urllib3_modules[name]))
