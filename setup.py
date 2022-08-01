from setuptools import (
    find_packages,
    setup,
)


REQUIREMENTS = [
    "requests >= 2.4.3",
    "typing-extensions",
]

DEV_REQUIREMENTS = [
    "bandit==1.7.1",  # Bandit 1.7.2 drops support for Python 3.6
    "black==22.*",
    "flake8==4.*",
    "isort==5.*",
    "pytest-cov==3.*",
    "pytest-vcr==1.*",
    "pytest==7.*",
    "twine==3.8.*",  # Twine 4.0+ drops support for Python 3.6
    "types-requests",
    "types-urllib3",
    "vcrpy==4.*",
    "wheel==0.37.*",
]

# packages incompatible with PyPy go here
CPYTHON_DEV_REQUIREMENTS = [
    "mypy==0.942",
]

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="easypost",
    version="7.4.0",
    description="EasyPost Shipping API Client Library for Python",
    author="EasyPost",
    author_email="support@easypost.com",
    url="https://easypost.com/",
    packages=find_packages(
        exclude=[
            "examples",
            "tests",
        ]
    ),
    install_requires=REQUIREMENTS,
    extras_require={
        "dev": DEV_REQUIREMENTS + CPYTHON_DEV_REQUIREMENTS,
        "pypy_dev": DEV_REQUIREMENTS,  # no cpython requirements
    },
    package_data={
        "easypost": ["py.typed"],
    },
    test_suite="test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Docs": "https://www.easypost.com/docs/api",
        "Tracker": "https://github.com/EasyPost/easypost-python/issues",
        "Source": "https://github.com/EasyPost/easypost-python",
    },
    python_requires=">=3.6, <4",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
)
