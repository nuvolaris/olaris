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

# deploy
nuv action list
task --list-all

task d F=openai/chat.py
task d F=mastrogpt/display.zip

# test demo
task d F=mastrogpt/demo.py
nuv invoke mastrogpt/demo
nuv invoke mastrogpt/demo -p input html
nuv invoke mastrogpt/demo -p input code
nuv invoke mastrogpt/demo -p input chess

# test display
chess = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1"
task d F=mastrogpt/display.zip
nuv invoke mastrogpt/display -p "message" "hello"
nuv invoke mastrogpt/display -p "html" "<h1>hello</h1>"
nuv invoke mastrogpt/display -p "code" "def sum(a,b):\n  return a + b\n" -p language python
nuv invoke mastrogpt/display -p chess  "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1"

# test extraction
task cli




