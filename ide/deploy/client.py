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

from pathlib import Path
from subprocess import Popen, PIPE
import os, os.path, json
import threading
import asyncio

def get_nuvolaris_config(key, default):
    try:
        dir = os.environ.get("NUV_PWD", "/do_not_exists")
        file = f"{dir}/package.json"
        info = json.loads(Path(file).read_text())
        return info.get("nuvolaris", {}).get(key, default)
    except:
        return default

def readlines(inp):
    for line in iter(inp.readline, ''):
        print(line, end='')

# serve web area
def launch(key, default):
    cmd = get_nuvolaris_config(key, default)
    proc = Popen(
        cmd, shell=True, 
        cwd=os.environ.get("NUV_PWD"), env=os.environ, 
        stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True
    )
    threading.Thread(target=readlines, args=(proc.stdout,)).start()
    threading.Thread(target=readlines, args=(proc.stderr,)).start()

def serve(): 
    launch("devel", "nuv ide serve")

def logs(): 
    launch("logs", "nuv activation poll")

# build
def build():
    deploy = get_nuvolaris_config("deploy", "true")
    proc = Popen(
        deploy, shell=True, 
        env=os.environ,
        cwd=os.environ.get("NUV_PWD"),
        stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True
    )
    proc.communicate()
