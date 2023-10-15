#!/bin/bash
echo '{ "text": "'"$$m"'"}' |\
curl -X POST \
     -H 'Content-type: application/json' \
     -d @- "$NUV_NOTIFY_SLACK_URL"
