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

def scan():
    # first look for requirements.txt and build the venv (add in set)
    deployments = set()
    packages = set()

    print("> Scan:")
    reqs =  glob("packages/*/*/requirements.txt") + glob("packages/*/*/package.json")
    # req = reqs[0]
    # from util.deploy.deploy import *
    for req in reqs:
        print(">> Requirements:", req)
        sp = req.split("/")
        act = build_zip(sp[1],sp[2])
        deployments.add(act)
        packages.add(sp[1])
        
    mains = glob("packages/*/*/index.js") + glob("packages/*/*/__main__.py")
    # main = mains[2]
    for main in mains: 
        print(">> Main:", main)
        sp = main.split("/")
        act = build_action(sp[1],sp[2])
        deployments.add(act)
        packages.add(sp[1])    

    singles = glob("packages/*/*.py") +  glob("packages/*/*.js")
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
