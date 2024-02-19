MAINS = ["__main__.py", "index.js"]

import os
from  os.path import exists, isdir
from subprocess import Popen

dry_run = False

def set_dry_run(b):
    global dry_run
    dry_run = b

def exec(cmd):
    global dry_run
    print("$", cmd)
    if not dry_run:
        Popen(cmd, shell=True, env=os.environ).wait()

def extract_args(files):
    res = []
    for file in files:
        #if dry_run:
        #    print(f": inspecting {file}")
        if exists(file):
            with open(file, "r") as f:
                for line in f.readlines():
                    if line.startswith("#-"):
                        res.append(line.strip()[1:])
                    if line.startswith("//-"):
                        res.append(line.strip()[2:])
    return res

package_done = set()

def deploy_package(package):
    global package_done
    # package args
    ppath = f"packages/{package}.args"
    pargs = " ".join(extract_args([ppath]))
    cmd = f"nuv package update {package} {pargs}"
    if not cmd in package_done:
        exec(cmd)
        package_done.add(cmd)

def build_zip(sp):
    exec(f"nuv ide _zip A={sp[1]}/{sp[2]}")
    res = sp[:-1]
    res[-1] += ".zip"
    return res

def build_action(sp):
    exec(f"nuv ide _action A={sp[1]}/{sp[2]}")
    res = sp[:-1]
    res[-1] += ".zip"
    return res

def deploy_action(sp):
    artifact = "/".join(sp)
    [name, typ] = sp[-1].rsplit(".", 1)
    package = sp[1]

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
def deploy(file):
    print(f"*** {file}")
    if isdir(file):
        for start in MAINS:
            sub = f"{file}/{start}"
            if exists(sub):
                file = sub
                break
    sp = file.split("/")
    if len(sp) > 3:
        build_zip(sp)
        sp = build_action(sp)
    deploy_action(sp)
