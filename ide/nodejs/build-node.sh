#!/bin/bash
DIR="${1:?directory}"
ZIP="${2:?zip file}"
cd "$DIR"
npm install
touch node_modules/.package-lock.json
if test -f "$ZIP"
then rm "$ZIP"
fi
zip -r "$ZIP" node_modules >/dev/null
ls -l $ZIP

