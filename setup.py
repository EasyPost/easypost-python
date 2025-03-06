from setuptools import (
    find_packages,
    setup,
)


REQUIREMENTS = [
    "requests >= 2.4.3",
]

DEV_REQUIREMENTS = [
    "bandit==1.7.*",  # v1.8 requires Python 3.9
    "black==23.*",
    "build==1.2.*",
    "flake8==5.*",  # v6 requires Python 3.9
    "isort==6.*",
    "mypy==1.15.*",
    "pdoc==14.*",  # v15 requires Python 3.9
    "pytest-cov==5.*",  # v6 requires Python 3.9
    "pytest-vcr==1.*",
    "pytest==8.*",
    "vcrpy==6.*",  # v7 requires Python 3.9
]

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="easypost",
    version="9.5.0",
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
    python_requires=">=3.8, <4",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
)
