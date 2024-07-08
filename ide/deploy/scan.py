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

from glob import glob
from .deploy import *
from .client import get_nuvolaris_config
from .config import DEFAULT_REQ_GLOBS, DEFAULT_MAIN_GLOBS, DEFAULT_SINGLES_GLOBS


def scan():
    """This function has two stages:\n
    Scan
    ===    
    A) Packages requirements\n
    Check for package requirements. It will look in a specific requirement file 
    (from web package.json) or a default set of requirements (requirements.txt, 
    composer.json etc. etc).\n
    For each requirement found, a zip is built calling the task:
    ``nuv ide util zip A={package}/{action}``\n
    The zip is added to actions (deployments); the directory is added to 
    packages (packages)\n
    B) Mains for packages\n
    After that, the scan continue checking the "mains". For each main, an
    action is built calling the task:\n
    ``nuv ide util action A={package}/{action}``\n
    where package is the base directory of main file and the action is the
    basename of the main file.\n
    C) Singles\n
    Finally the scan will take care of single file functions\n
    
    Deploy
    ===
    Each package is deployed with the command:\n
    ``nuv package update {package} {pargs}``\n
    Each deployment is deployed with the command:\n
    ``nuv action update {package}/{name} {artifact} {args}``\n
    """

    # first look for requirements.txt and build the venv (add in set)
    deployments = set()
    packages = set()

    print("> Scan:")
    package_globs = get_nuvolaris_config("requirements", DEFAULT_REQ_GLOBS)
    reqs = list()

    for pkg_glob in package_globs:
        items = glob(pkg_glob)
        # extend first list without duplicates
        reqs.extend(x for x in items if x not in reqs)

    # req = reqs[0]
    # from util.deploy.deploy import *
    for req in reqs:
        print(">> Requirements:", req)
        sp = req.split("/")
        act = build_zip(sp[1], sp[2])
        deployments.add(act)
        packages.add(sp[1])

    # => MAINS
    mains_globs = get_nuvolaris_config("mains", DEFAULT_MAIN_GLOBS)
    mains = list()
    for main_glob in mains_globs:
        items = glob(main_glob)
        # extend first list without duplicates
        mains.extend(x for x in items if x not in mains)

    # main = mains[2]
    for main in mains:
        print(">> Main:", main)
        sp = main.split("/")
        act = build_action(sp[1], sp[2])
        deployments.add(act)
        packages.add(sp[1])

    # => SINGLES

    singles_globs = get_nuvolaris_config("singles", DEFAULT_SINGLES_GLOBS)
    singles = list()
    for single_glob in singles_globs:
        items = glob(single_glob)
        singles.extend(x for x in items if x not in singles)

    # single = singles[0]
    for single in singles:
        print(">> Action:", single)
        sp = single.split("/")
        deployments.add(single)
        packages.add(sp[1])

    print("> Deploying:")
    for package in packages:
        print(">> Package:", package)
        deploy_package(package)

    for action in deployments:
        print(">>> Action:", action)
        deploy_action(action)
