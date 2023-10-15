import sys, os, subprocess, json

argv = sys.argv

if len(argv) < 3:
    print("usage: <directory> <prefix> <id>")
    sys.exit(1)

if not "NTFY_RAW" in os.environ:
    print("this script but be invoked by nfty - missing NTFY_RAW env var")
    sys.exit(1)

# params
dir = argv[1]
prefix = argv[2]
id = argv[3]
env = os.environ.copy()
env['NUV_ROOT_PLUGIN'] = dir
os.chdir(dir)

# load command from message
data = json.loads(os.environ["NTFY_RAW"])
if 'attachment' in data:
    url = data['attachment'].get('url')
    if url is None:
        print("no url found")
        sys.exit(1)
    cmd = subprocess.check_output(["curl", "-sL", url]).decode("utf-8")    
elif 'message' in data:
    cmd = data['message']
else:
    print("no message found")
    sys.exit(1)

# execute command and format output
r = subprocess.run(cmd, shell=True, capture_output=True, env=env)

out = r.stdout.decode("UTF-8")
if not out.endswith("\n"):
    out += "\n"

err = r.stderr.decode("UTF-8")
if len(err) >0:
    out += "=== STDERR ===\n%s" % err

if not out.endswith("\n"):
    out += "\n"

file = None
if len(out) > 4000:
    file = out
    out = "--- long ---"

message = "\n".join([ f"{id} | {x}" for x in out.strip().split("\n")])

if r.returncode == 0:
    message += f"\n{id} +- OK\n"
else:
    message += f"\n{id} +- ERROR: {r.returncode}\n"

with open(f"{prefix}_title", "w") as f: 
    if len(cmd) > 80:
        cmd = cmd[0:80]+"..."
    f.write(cmd)
with open(f"{prefix}_message", "w") as f: 
    f.write(message)
if not file is None:
    with open(f"{prefix}_file", "w") as f: 
        f.write(file)
