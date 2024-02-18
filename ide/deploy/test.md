#DRY="F=-n"
DRY=""

cd /workspaces/all/python-starter
nuv ide deploy A=mastrogpt/index.py $DRY
$ nuv package update mastrogpt 
$ nuv action update mastrogpt/index packages/mastrogpt/index.py --web true

nuv ide deploy A=mastrogpt/display $DRY
$ nuv ide enviromment A=mastrogpt/display
$ nuv ide compile A=mastrogpt/display
$ nuv package update mastrogpt 
$ nuv action update mastrogpt/display packages/mastrogpt/display.zip --web true --kind python:default

nuv ide deploy A=openai/chat $DRY
$ nuv ide enviromment A=openai/chat
$ nuv ide compile A=openai/chat
$ nuv package update openai 
$ nuv action update openai/chat packages/openai/chat.zip 

cd /workspaces/all/nodejs-starter
nuv ide deploy A=openai/completions.js $DRY
$ nuv action update openai/completions packages/openai/completions.js --web true --kind nodejs:default --param OPENAI_API_KEY $OPENAI_API_KEY --param OPENAI_API_HOST $OPENAI_API_HOST

nuv ide deploy A=examples/multifile $DRY
$ nuv ide enviromment A=examples/multifile
$ nuv ide compile A=examples/multifile
$ nuv package update examples 
$ nuv action update examples/multifile packages/examples/multifile.zip --web true --kind nodejs:default

nuv ide deploy A=examples/withreqs $DRY
$ nuv ide enviromment A=examples/multifile
$ nuv ide compile A=examples/multifile
$ nuv package update examples 
$ nuv action update examples/multifile packages/examples/multifile.zip --web true --kind nodejs:default

