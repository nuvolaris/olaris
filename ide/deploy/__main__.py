import argparse, json, sys, os, socket
from os.path import isdir, exists
from pathlib import Path
from .scan import scan
from .watch import watch
from .deploy import set_dry_run, deploy

def main():
    # check port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("127.0.0.1", 8080)) == 0:
            print("deployment mode already active")
            return

    parser = argparse.ArgumentParser(description='Deployer')
    parser.add_argument('directory', help='The mandatory first argument')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Dry Run', required=False)
    parser.add_argument('-d', '--deploy', action='store_true', help='Deploy', required=False)
    parser.add_argument('-w', '--watch', action='store_true', help='Watch for changes', required=False)
    parser.add_argument('-s', '--single', type=str, default="", help='Deploy a single action, either a single file or a directory.')

    args = parser.parse_args()
    set_dry_run(args.dry_run)
    os.chdir(args.directory)
    
    #try: 
    #  config = json.loads(Path("nuvolaris.json").read_text())
    #except Exception as e:
    #  print("cannot read nuvolaris.json current directory: %s" % e)
    #  sys.exit(1)
    
    if args.watch:
        scan()
        watch()
        return
    elif args.deploy:
        scan()
        return
    elif args.single != "":        
        action = args.single
        if not action.startswith("packages/"):
            action = f"packages/{action}"
        if not exists(action):
            print(f"action {action} not found: must be either a file or a directory under packages")
            return
        print(f"Deploying {action}")
        deploy(action)
        return
    else:
        parser.print_usage()

if __name__ == "__main__":
    main()
