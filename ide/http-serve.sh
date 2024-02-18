#!/bin/bash
if test -e /tmp/nuv-poll.pid
then
    PID=$(cat /tmp/nuv-poll.pid 2>/dev/null)
    if test -e /proc/$PID
    then kill -9 $PID 
    fi
fi

if test -e /tmp/http-serve.pid
then
    PID=$(cat /tmp/http-serve.pid 2>/dev/null)
    if test -e /proc/$PID
    then kill -9 $PID
    fi
fi
MIME="$PWD/mime.types"
if test -d "$1"
then 
    echo $$ >/tmp/http-serve.pid
    nuv -wsk activation poll & echo $! >/tmp/nuv-poll.pid
    exec http-server -a 127.0.0.1 "$1" -c-1 --mimetypes "$MIME" -P $NUVDEV_HOST
else echo "Directory not found: $1"
fi