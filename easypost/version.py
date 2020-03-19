import pkg_resources

VERSION_FILE = pkg_resources.resource_stream('easypost', '../VERSION')
VERSION = VERSION_FILE.read().decode('utf-8').strip()
VERSION_FILE.close()

if '-' in VERSION:
    VERSION_INFO = tuple([int(v) for v in VERSION.split('-')[0].split('.')] + VERSION.split('-')[1:])
else:
    VERSION_INFO = tuple(int(v) for v in VERSION.split('.'))
