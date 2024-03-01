#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

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