VERSION = '5.1.2'

if '-' in VERSION:
    VERSION_INFO = tuple([int(v) for v in VERSION.split('-')[0].split('.')] + VERSION.split('-')[1:])
else:
    VERSION_INFO = tuple(int(v) for v in VERSION.split('.'))
