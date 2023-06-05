#!/usr/bin/env bash

# This script is used to adjust the examples repo style guide for use on the Python client library.

# Ref: sed to work on both Unix and MacOS: https://stackoverflow.com/a/44864004

# Replace extend-ignore = E203, F821 with extend-ignore = E203 in .flake8 (want to enforce F821 in the Python client library)
sed -i.bak 's/extend-ignore = E203, F821/extend-ignore = E203/g' .flake8 && rm .flake8.bak
