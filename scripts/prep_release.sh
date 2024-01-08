#!/bin/bash

# This script is used to prepare a release of the project.
# This scripts expects to use the GNU version of sed, not the BSD/MacOS version.
# For MacOS via Homebrew: https://formulae.brew.sh/formula/gnu-sed

NEW_VERSION=$1

# Collect date from second argument if it exists, otherwise use today's date as %Y-%m-%d
NEW_VERSION_DATE=$2
if [ -z "$NEW_VERSION_DATE" ]; then
    NEW_VERSION_DATE=$(date +%Y-%m-%d)
fi

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: $0 <new version>"
    exit 1
fi

CHANGELOG_TEXT_TO_REPLACE="^## [n,N]ext [r,R]elease"
NEW_CHANGELOG_TEXT="## v$NEW_VERSION ($NEW_VERSION_DATE)"

# Update version in setup.py
sed -i -r "s/version=\".*\",/version=\"$NEW_VERSION\",/" setup.py

# Update version in easypost/constant.py
# Use regex ^ to avoid overriding API_VERSION in the same file
sed -i -r "s/^VERSION = \".*\"/VERSION = \"$NEW_VERSION\"/" easypost/constant.py

# Update version in CHANGELOG.md
sed -i -r "s/$CHANGELOG_TEXT_TO_REPLACE/$NEW_CHANGELOG_TEXT/" CHANGELOG.md
