<!--
  ~ Licensed to the Apache Software Foundation (ASF) under one
  ~ or more contributor license agreements.  See the NOTICE file
  ~ distributed with this work for additional information
  ~ regarding copyright ownership.  The ASF licenses this file
  ~ to you under the Apache License, Version 2.0 (the
  ~ "License"); you may not use this file except in compliance
  ~ with the License.  You may obtain a copy of the License at
  ~
  ~   http://www.apache.org/licenses/LICENSE-2.0
  ~
  ~ Unless required by applicable law or agreed to in writing,
  ~ software distributed under the License is distributed on an
  ~ "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  ~ KIND, either express or implied.  See the License for the
  ~ specific language governing permissions and limitations
  ~ under the License.
-->

#
DRY="F=-n"
DRY=""

cd /workspaces/all/python-starter
nuv ide _clean A=mastrogpt/index.py 
nuv ide deploy A=mastrogpt/index.py FL=-n
$ nuv package update mastrogpt 
$ nuv action update mastrogpt/index packages/mastrogpt/index.py --web true
nuv ide deploy A=mastrogpt/index.py


nuv ide _clean A=mastrogpt/display
nuv ide deploy A=mastrogpt/display FL=-n
$ nuv ide _zip A=mastrogpt/display
$ nuv ide _action A=mastrogpt/display
$ nuv package update mastrogpt 
$ nuv action update mastrogpt/display packages/mastrogpt/display.zip --web true --kind python:default
nuv ide _clean A=mastrogpt/display
nuv ide deploy A=mastrogpt/display
nuv ide deploy A=mastrogpt/display

nuv ide _clean A=openan/chat
nuv ide deploy A=openai/chat FL=-n
$ nuv ide _zip A=openai/chat
$ nuv ide _action A=openai/chat
$ nuv package update openai 
$ nuv action update openai/chat packages/openai/chat.zip --web true --kind python:default
nuv ide _clean A=openai/chat
nuv ide deploy A=openai/chat

cd /workspaces/all/nodejs-starter
nuv ide deploy A=openai/completions.js FL=-n
$ nuv package update openai 
$ nuv action update openai/completions packages/openai/completions.js --web true --kind nodejs:default --param OPENAI_nuv ide deploy A=openai/completions.js
nuv ide deploy A=openai/completions.js

nuv ide deploy A=examples/multifile FL=-n
$ nuv ide _zip A=examples/multifile
$ nuv ide _action A=examples/multifile
$ nuv package update examples 
$ nuv action update examples/multifile packages/examples/multifile.zip --web true --kind nodejs:default
nuv ide deploy A=examples/multifile

nuv ide deploy A=examples/withreqs FL=-n
$ nuv ide _zip A=examples/withreqs
$ nuv ide _action A=examples/withreqs
$ nuv package update examples 
$ nuv action update examples/withreqs packages/examples/withreqs.zip --web true --kind nodejs:default
nuv ide deploy A=examples/withreqs

