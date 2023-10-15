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

# nuv remote

Nuv remote is a remote task executor and it is based on [nuv](https://github.com/nuvolaris/nuv)

The basic idea is:

- You write the commands you want as tasks under olaris-ops
- Then you invoke and execute them in the remote hosts, even multiple hosts at the same time.
- All the output are collected in a logger and that you can read

You select the hosts to run the command, and then execute commands and task in them.

Hosts are named following a convention, have some environment variables configured and run `nuv remote server`

You write the tasks to execute under the olaris-ops folder as a `nuv` , and they are uploaded to all the remote server and executed remotely.

There are some prerequisites and conventions to follow.

# How it works

Topics:

- prerequisites
- how to name and select hosts
- setup the server
- setup the client
- start the logger
- execute remote shell commands
- remote task distribution
- remote task execution

## Select hosts

Each host managed by `nuv remote` must have the hostname in the format: `<node-type>-<node-num>-<group-num>-<cloud>`

The name is essential as it is used to select them.

- `<node-type>` is a string identifiying a node type (`hub`, `mst`, `wrk` etc)
- `<node-num>` is a number identifying a node 
- `<group-num>` is a number identifying a group of nodes.
- `<cloud>` is string identifying a cloud (`aws`, `gcp`, `hz`, `cc`) etc

For example:  

- `hub-1-1-hz` (hub 1, group 1 in cloud hetzner) 
- `mst-1-1-aws` (master 1 group 1 in cloud aws g) 
- `wrk-1-2-gcp` (worker 2 in cloud gcp group 1)

You can now execute commands and tasks using the host selector in the format:

`[<type>][-][<group>][-][<node>]`

Each part if omitted is replaced with `*`, and `-` are added to became a wildcard in format `<type>-<group>-<node>`.

At the end `-` and the current cloud suffix will be added. If the current cloud is `aws`:

- `-` expands to `*-*-*-aws`
- `hub`  expands to `hub-*-*-aws`
- `mst-1` expands to `mst-1-1-aws`
- `wrk--1` expands tp `wrk-*-1-aws`

## Setup the server 

We use `ntfy.sh` to connect servers and clients.

Setup an account on ntfy.sh (or self-host it) Then you can create two topics, one identified as `<out-topic>` for sending commands, and another identified as `<in-topic>` for retrieving results.  Then generate an authentication token `<ntfy-token>` able to read and write *privately* on those tokens

Connect to the server you want to use, download and install latest `nuv`,
then install a service with

```
nuv remote server install CLOUD=<cloud> TOKEN=<ntfy-token> IN=<in-topic> OUT=<out-topic>
```

# Setup the Client

Now you can use the client to control the servers

You should execute the client from the `saas` project home directory.

You need to configure servers remote and tokens:

```
nuv -config NUV_REMOTE_NFTY_TOKEN=<ntfy-token>
nuv -config NUV_REMOTE_NTFY_TOPIC_IN=<in-topic>
nuv -config NUV_REMOTE_NTFY_TOPIC_OUT=<out-topic>
```

For simplicity of execution add the following aliases in .bashrc

alias nrt="nuv remote client task"
alias nrs="nuv remote client shell"
alias nrsel="nuv remote client select"

Commands are always restricted to one cloud, so you should select the cloud (that is a suffix for all the hostnames) you want to manage. 

Example:

```
nrsel aws
```

## Start the logger

To see all the outputs you need to start a logger, so you will need two terminals: you will execute commands from the cli but the result is asyncronous so to see the results you need to launch the logger in another terminal 

Start in another terminal:

```
nuv remote logger
```

## Remote command Execution

Now you can execute remotely shell commands with:

`nrs <host-selector> <command>`

where `<host-selector>`  allows to select the commands where to run a task.

It will execute the shell command with the args in the hosts matching the expanded host selector.

**NOTE** If the command has parameters with `-`, you have to use

`nrs <host-selector> -- <command>`

Example:

```
$ nrs - hostname 
# executes hostname on all hosts
$ nrs mst -- df -h
# execute `df -h` on all the `mst` hosts
```

## Remote task distribution

You can execute tasks in selected servers, distributing automatically a `nuv` plugin in all the servers.

Distribution happens automatically before execution of a remote task when you change a task. 

You can force a distribution with command `nuv remote client refresh`.  

The logger helps with the distriution. When it starts, it forces a referesh and also when a new server join a distribution.

So to be sure the task distribution works, always run the logger before executing commands.

## Remote task execution

You can execute task remotely with `nrt <host-selector> <tasks-with-parameters...>`

It will let you to execute the task *using the subcommad corresponding to the host type*.

For example:

```
nrt wrk-1 check
```

Then the host selector will be expanded: `wrk-1-*-aws` (we assume here cloud is `aws`)

Then the host `<type>` (in our case `wrk`) will be extracted.

Then finally command: `nuv ops wrk check` will be executed in all the hosts matching the host selector (in this case all the `wrk` in `aws` of the group 1).

**Please note it will always use a subcommand corresponding to the node type.**

In a plugin (like `ops`) your tasks are grouped  by subcommand. For example

```
$ nuv ops
* all:        commands for all
* host:       ubuntu host
* hub:        commands for the hub
* mst:        commands for the master
* wrk:        commands for the worker
```

When you invoke the remote task, it will execute tasks under the subcommand corresponding to the host type you selected.

If you select all the hosts `-` then the `all` subcommand will be used instead.
