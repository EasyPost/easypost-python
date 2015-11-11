import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'easypost'))
import importer
import version

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

# Get simplejson if we don't already have json
install_requires = ['requests >= 1.0.0', 'six']
try:
    importer.import_json()
except ImportError:
    install_requires.append('simplejson')

try:
    import json
    _json_loaded = hasattr(json, 'loads')
except ImportError:
    pass

setup(
    name='easypost',
    version=version.VERSION,
    description='EasyPost Shipping API Client Library for Python',
    author='Sawyer Bateman',
    author_email='support@easypost.com',
    url='https://easypost.com/',
    packages=['easypost'],
    package_data={'easypost': ['../VERSION']},
    install_requires=install_requires,
    test_suite='test'
)
