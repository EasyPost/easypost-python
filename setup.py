import io
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

REQUIREMENTS = [
    "requests >= 2.4.3",
    "six",
]

DEV_REQUIREMENTS = [
    "black",
    "configparser<5",  # 5.0.0 removes python 2.x support
    "flake8",
    "isort",
    "mock==3.0.5",  # >3.0.5 removes python 2.x support
    "pytest-cov==2.8.1",
    "pytest-vcr==1.*",
    "pytest==4.6.*",
    "pytz",
    "setuptools>=42,<45",  # 45.0.0 removes python 2.x support
    "vcrpy==3.*",  # 4.x removes python 2.x support
    "zipp==0.5.*",  # zipp after 0.5 tries to install its own setuptools at build time, which fails on python 2.7
]


if sys.version_info < (3, 0):
    long_description_open = io.open
else:
    long_description_open = open

with long_description_open("README.md", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="easypost",
    version="6.0.0",
    description="EasyPost Shipping API Client Library for Python",
    author="EasyPost",
    author_email="support@easypost.com",
    url="https://easypost.com/",
    packages=["easypost"],
    install_requires=REQUIREMENTS,
    extras_require={
        "dev": DEV_REQUIREMENTS,
    },
    test_suite="test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Docs": "https://www.easypost.com/docs/api",
        "Tracker": "https://github.com/EasyPost/easypost-python/issues",
        "Source": "https://github.com/EasyPost/easypost-python",
    },
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4",
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
    ],
)
