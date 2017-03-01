try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = [
    'requests >= 1.0.0'
    'six'
]


with open('VERSION', 'r') as f:
    version = f.read().strip()


setup(
    name='easypost',
    version=version,
    description='EasyPost Shipping API Client Library for Python',
    author='EasyPost',
    author_email='support@easypost.com',
    url='https://easypost.com/',
    packages=['easypost'],
    package_data={'easypost': ['../VERSION']},
    install_requires=install_requires,
    test_suite='test',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ]
)
