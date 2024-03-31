from pathlib import Path
import os, os.path, json
from subprocess import Popen

def get_nuvolaris_config(key):
    try:
        dir = os.environ.get("NUV_PWD", "/do_not_exists")
        file = f"{dir}/package.json"
        info = json.loads(Path(file).read_text())
        return info.get("nuvolaris", {}).get(key)
    except:
        return None
    
# serve web area
def serve():
    devel = get_nuvolaris_config("devel")
    if devel is None:
        devel = "nuv ide serve"
    Popen(devel, shell=True, cwd=os.environ.get("NUV_PWD"), env=os.environ)

def build():
    deploy = get_nuvolaris_config("deploy")
    if deploy is not None:
        Popen(deploy, shell=True, cwd=os.environ.get("NUV_PWD"), env=os.environ)