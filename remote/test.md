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

# alias
alias ns="nuv saas"
alias nrc="nuv remote client"
alias nrt="nuv remote client task"
alias nrs="nuv remote client shell"

# setvar
A_B64=$(echo hello | base64 -w0)

BIG="$(seq 1 1000v | base64 | fold -w 80)"
BIG_B64=$(echo $BIG | base64 -w0)

nrs dev hostname

nrs dev nuv remote setvar VAR=A VAL_B64=$A_B64
nrs dev -- nuv remote getvar VAR=A

nrs dev nuv remote setvar VAR=BIG VAL_B64=$BIG_B64
nrs dev -- nuv remote getvar VAR=BIG

