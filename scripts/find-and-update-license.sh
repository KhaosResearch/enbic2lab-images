#!/usr/bin/env bash

set -e

for file in $(find components -type f -iname "annotation*.json"); do
    echo "Checking: $file"

    LICENSE=$(jq -r '.license' $file)
    if [ "$LICENSE" = "MIT" ]; then
        echo  "Wrong license found in $file"
        sed -i '' -e 's/"mit-licensed"/"cc by-nc-nd 4.0", "by-nc-nd"/' $file
        sed -i '' -e 's/"license": "MIT",/"license": "cc by-nc-nd 4.0",/' $file
    fi

    if [ "$LICENSE" = "cc by-nc-nd 4.0" ]; then
        cp LICENSE $(dirname $file)
    fi
done