import io
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = [
    'requests >= 1.0.0',
    'six'
]


if sys.version_info < (3, 0):
    long_description_open = io.open
else:
    long_description_open = open

with long_description_open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='easypost',
    version='5.1.2',
    description='EasyPost Shipping API Client Library for Python',
    author='EasyPost',
    author_email='support@easypost.com',
    url='https://easypost.com/',
    packages=['easypost'],
    install_requires=install_requires,
    test_suite='test',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls={
        'Docs': 'https://www.easypost.com/docs/api',
        'Tracker': 'https://github.com/EasyPost/easypost-python/issues',
        'Source': 'https://github.com/EasyPost/easypost-python',
    },
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ]
)
