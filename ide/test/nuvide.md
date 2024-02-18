export NUV_ROOT=/workspaces/all/olaris
cd /workspaces/all

alias ni="nuv ide"
ni
ni login
ni setup
cd /workspaces/all/python-starter
ni serve

# deploy
ni deploy

ni build DIR=

localizzare i packages.json
e i virtualenv
environments
generate gli environment prima
farli dipendere dal requirements.txt
