from setuptools import (
    find_packages,
    setup,
)


REQUIREMENTS = [
    "requests >= 2.4.3",
]

DEV_REQUIREMENTS = [
    "bandit==1.7.5",
    "black==23.*",
    "build==1.0.*;python_version>='3.8'",  # TODO: remove python pin when 3.7 is dropped
    "urllib3==1.*",  # TODO: Pinned because vcrpy did a dumb and didn't pin urllib3
    "flake8==5.*",  # TODO: flake8 v6 requires Python 3.8.1+
    "isort==5.*",
    "mypy==1.4.*",  # TODO: mypy v1.5 requires Python 3.8+
    "pdoc==13.*",  # TODO: pdoc v14 requires Python 3.8+
    "pytest-cov==4.*",
    "pytest-vcr==1.*",
    "pytest==7.*",
    "twine==4.*",
    "types-requests",
    "types-urllib3",
    "vcrpy==4.*",  # TODO: vcrpy v5 requires Python 3.8+
]

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="easypost",
    version="9.3.0",
    description="EasyPost Shipping API Client Library for Python",
    author="EasyPost",
    author_email="support@easypost.com",
    url="https://easypost.com/",
    packages=find_packages(
        exclude=[
            "docs",
            "examples",
            "tests",
        ]
    ),
    install_requires=REQUIREMENTS,
    extras_require={
        "dev": DEV_REQUIREMENTS,
    },
    package_data={
        "easypost": ["py.typed"],
    },
    test_suite="test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Docs": "https://docs.easypost.com",
        "Tracker": "https://github.com/EasyPost/easypost-python/issues",
        "Source": "https://github.com/EasyPost/easypost-python",
    },
    python_requires=">=3.7, <4",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
)
