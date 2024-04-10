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
import os, os.path, json
from subprocess import Popen
import asyncio

def get_nuvolaris_config(key):
    try:
        dir = os.environ.get("NUV_PWD", "/do_not_exists")
        file = f"{dir}/package.json"
        info = json.loads(Path(file).read_text())
        return info.get("nuvolaris", {}).get(key)
    except:
        return None
 
# serve web area
async def serve():
    devel = get_nuvolaris_config("devel")
    if devel is None:
        devel = "nuv ide serve"
    print(devel)
    #Popen(devel, shell=True, cwd=os.environ.get("NUV_PWD"), env=os.environ)
    pwd = os.environ.get("NUV_PWD")
    cmd = f"cd '{pwd}' ; {devel}"
    proc = await asyncio.create_subprocess_shell(cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

# build
def build():
    deploy = get_nuvolaris_config("deploy")
    if deploy is not None:
        Popen(deploy, shell=True, cwd=os.environ.get("NUV_PWD"), env=os.environ)