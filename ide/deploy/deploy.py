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

import os
from os.path import exists, isdir
from subprocess import Popen
from .config import MAINS

dry_run = False


def set_dry_run(b: bool):
    """Set global dry run

    Args:
        b (bool): true for dry run enabled
    """
    global dry_run
    dry_run = b


def exec(cmd: str):
    """Exec a shell command and wait for it to complete.
    If dryrun is set, the command is not executed.

    Args:
        cmd (str): command line to execue
    """
    global dry_run
    print("$", cmd)
    if not dry_run:
        Popen(cmd, shell=True, env=os.environ).wait()


def extract_args(files: list) -> list:
    """Extract openwhisk args from files

    Args:
        files (list): the list of files to inspect

    Returns:
        list: a list of parameters
    """
    res = []
    for file in files:
        # if dry_run:
        #  print(f": inspecting {file}")
        if exists(file):
            with open(file, "r") as f:
                for line in f.readlines():
                    if line.startswith("#-"):
                        res.append(line.strip()[1:])
                    if line.startswith("//-"):
                        res.append(line.strip()[2:])
    return res


package_done = set()


def deploy_package(package: str):
    """Deploy a package on nuvolaris

    Args:
        package (str): the name of package
    """
    global package_done
    # package args
    ppath = f"packages/{package}.args"
    pargs = " ".join(extract_args([ppath]))
    cmd = f"nuv package update {package} {pargs}"
    if not cmd in package_done:
        exec(cmd)
        package_done.add(cmd)


def build_zip(package: str, action: str) -> str:
    """Builds a zip for the package / action

    Args:
        package (str): package
        action (str): action

    Returns:
        str: the path of the built zip file
    """
    exec(f"nuv ide util zip A={package}/{action}")
    return f"packages/{package}/{action}.zip"


def build_action(package: str, action: str) -> str:
    """Invoke the nuv ide util action command on package / action

    Args:
        package (_type_): _description_
        action (_type_): _description_

    Returns:
        str: the zip with the built action
    """
    exec(f"nuv ide util action A={package}/{action}")
    return f"packages/{package}/{action}.zip"


def deploy_action(artifact: str):
    """Deploy an artifact calling nuv action update
    """
    try:
        sp = artifact.split("/")
        [name, typ] = sp[-1].rsplit(".", 1)
        package = sp[1]
    except:
        print("! cannot deploy", artifact)
        return

    deploy_package(package)

    if typ == "zip":
        base = artifact[:-4]
        to_inspect = [f"{base}/{x}" for x in MAINS]
    else:
        to_inspect = [artifact]

    args = " ".join(extract_args(to_inspect))
    exec(f"nuv action update {package}/{name} {artifact} {args}")


"""
file = "packages/deploy/hello.py"
file = "packages/deploy/multi.zip"
file = "packages/deploy/multi/__main__.py"
file = "packages/deploy/multi/requirements.txt"
"""


def deploy(file: str):
    """Deploy a package on nuvolaris

    Args:
        file (str): the file to deploy
    """
    # print(f"*** {file}")
    if isdir(file):
        for start in MAINS:
            sub = f"{file}/{start}"
            if exists(sub):
                file = sub
                break
    sp = file.split("/")
    if len(sp) > 3:
        build_zip(sp[1], sp[2])
        file = build_action(sp[1], sp[2])
    deploy_action(file)
