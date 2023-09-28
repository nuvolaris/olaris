import sys, os, subprocess


argv = ["-", ".", "xxx", "ls", "-l"]
argv = sys.argv

if len(argv) < 4:
    print("usage: <directory> <prefix> <command>...")
    os.exit(1)

dir = argv[1]
prefix = argv[2]
cmd = argv[3:]
pid = os.getpid()
os.chdir(dir)

title = " ".join(cmd)

# execute command and format output
r = subprocess.run(cmd, shell=True, capture_output=True)
out = r.stdout.decode("UTF-8")
if not out.endswith("\n"):
    out += "\n"
err = r.stderr.decode("UTF-8")
if len(err) >0:
    out += "=== ERROR:\n"+err

tag = "OK" if r.returncode == 0 else "FAIL"

message = "\n".join([ f"[{pid}] {x}" for x in out.strip().split("\n")])
file = ""

if len(message) > 4000:
    file = message
    message = "--- long ---"

with open(f"{prefix}_title", "w") as f: 
    f.write(title)
with open(f"{prefix}_tag", "w") as f: 
    f.write(tag)
with open(f"{prefix}_message", "w") as f: 
    f.write(message)
if len(file) >0:
    with open(f"{prefix}_file", "w") as f: 
        f.write(file)



cmd = ["ls", "'-l'"]
print("chdir ", sys.argv[1])
os.chdir(dir)
print("exec",  )


# todo

