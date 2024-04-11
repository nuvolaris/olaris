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

SKIPDIR = ["virtualenv", "node_modules", "__pycache__"]

import watchfiles
import asyncio
import os.path
import signal

from .deploy import deploy
from .client import serve, logs

def check_and_deploy(change):
    cur_dir_len = len(os.getcwd())+1
    change_type, path = change
    src = path[cur_dir_len:]
    print(f"{change_type}: {src}")
    # only modified
    if change_type != watchfiles.Change.modified: return
    # no directories
    if os.path.isdir(src): return
    # no missing files
    if not os.path.exists(src): return
    # no generated directories
    for dir in src.split("/")[:-1]:
        if dir in SKIPDIR: return
    # no generated files
    if src.endswith(".zip"): return
    # now you can deploy
    deploy(src)

async def redeploy():
    print("redeploy")
    iterator = watchfiles.awatch("packages", recursive=True)
    try:
        async for changes in iterator:
            for change in changes:
                check_and_deploy(change)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    except:
        print("Exception")

def watch():
    # start web server
    serve()
    # show logs
    logs()

    loop = asyncio.get_event_loop()
    task = loop.create_task(redeploy())
    def end_loop():
        print("Ending task.")
        task.cancel()
    loop.add_signal_handler(signal.SIGTERM, end_loop)

    try:
        loop.run_until_complete(task)
    except:
        pass
    finally:
        loop.stop()
        loop.close()
