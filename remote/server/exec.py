import sys, os, subprocess

#argv = ["-", ".", "xxx", "ls", "-l"]
argv = sys.argv

if len(argv) < 4:
    print("usage: <directory> <prefix> <id> <command>...")
    os.exit(1)

dir = argv[1]
prefix = argv[2]
id = argv[3]
cmd = " ".join(argv[4:])
pid = os.getpid()
env = os.environ.copy()
env['NUV_ROOT_PLUGIN'] = dir
os.chdir(dir)

# execute command and format output
r = subprocess.run(cmd, shell=True, capture_output=True, env=env)
out = r.stdout.decode("UTF-8")
if not out.endswith("\n"):
    out += "\n"

err = r.stderr.decode("UTF-8")
if len(err) >0:
    out += "=== ERROR:\n"+err

if not out.endswith("\n"):
    out += "\n"

if r.returncode != 0:
    out += "=== STATUS: %d\n" % r.returncode

message = "\n".join([ f"{id}:{x}" for x in out.strip().split("\n")])
file = ""

if len(message) > 4000:
    file = message
    message = "--- long ---"

with open(f"{prefix}_title", "w") as f: 
    f.write(cmd)
with open(f"{prefix}_message", "w") as f: 
    f.write(message)
if len(file) >0:
    with open(f"{prefix}_file", "w") as f: 
        f.write(file)
