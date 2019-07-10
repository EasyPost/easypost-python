import pkg_resources


VERSION = pkg_resources.resource_stream('easypost', '../VERSION').read().decode('utf-8').strip()

if '-' in VERSION:
    VERSION_INFO = tuple([int(v) for v in VERSION.split('-')[0].split('.')] + VERSION.split('-')[1:])
else:
    VERSION_INFO = tuple(int(v) for v in VERSION.split('.'))
