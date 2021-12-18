import io
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import easypost._info as package_info
from easypost._version import VERSION

from datetime import date


if sys.version_info < (3, 0):
    long_description_open = io.open
else:
    long_description_open = open

with long_description_open("README.md", encoding="utf-8") as f:
    long_description = f.read()

COPYRIGHT = package_info.COPYRIGHT
if not COPYRIGHT:
    COPYRIGHT = "Copyright © {0} - {1}".format(date.today().year, package_info.AUTHOR)

setup(
    name=package_info.TITLE,
    packages=[package_info.TITLE],
    version=VERSION,
    license=package_info.LICENSE,
    description=package_info.DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=package_info.AUTHOR,
    author_email=package_info.AUTHOR_EMAIL,
    url=package_info.URL,
    download_url='https://github.com/{0}/archive/refs/tags/{1}.tar.gz'.format(os.environ["GITHUB_REPO"], {os.environ["TAG"]}),
    install_requires=package_info.INSTALL_REQUIREMENTS,
    test_suite="test",
    project_urls={
        "Docs": "https://www.easypost.com/docs/api",
        "Tracker": "https://github.com/{0}/issues".format(os.environ['GITHUB_REPO']),
        "Source": "https://github.com/{0}".format(os.environ['GITHUB_REPO']),
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
