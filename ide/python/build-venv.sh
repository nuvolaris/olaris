#!/bin/bash
DIR="${1:?directory}"
ZIP="${2:?zip file}"
cd "$DIR"
virtualenv virtualenv
source virtualenv/bin/activate
pip install --upgrade pip
pip install -r  requirements.txt
virtualenv/bin/python -m pip uninstall -y -q setuptools wheel pip
touch virtualenv/bin/activate
if test -f "$ZIP"
then rm "$ZIP"
fi
zip -r "$ZIP" virtualenv >/dev/null
ls -l $ZIP

