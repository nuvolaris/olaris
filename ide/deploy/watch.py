# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

SKIPDIR = ["virtualenv", "node_modules", "__pycache__"]

import os, sys, signal, os.path
from subprocess import Popen
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .deploy import deploy
from .client import serve

class ChangeHandler(FileSystemEventHandler):
    """Logs all the events captured."""
    
    last_modified = {}

    def on_any_event(self, event):
        ## filter what is needed
        # only modified
        if event.event_type != "modified": return
        # no directories
        if event.is_directory: return
        src = event.src_path
        # no missing files
        if not os.path.exists(src): return
        # no generated directories
        for dir in src.split("/")[:-1]:
            if dir in SKIPDIR: return
        # no generated files
        if src.endswith(".zip"): return

        # cache last modified to do only once
        cur = os.path.getmtime(src)
        if self.last_modified.get(src, 0) == cur:
            return
        self.last_modified[src] = cur
        deploy(src)

def watch():
    observer = Observer()
    event_handler = ChangeHandler()
    observer.schedule(event_handler, "packages", recursive=True)
    #observer.schedule(event_handler, "web", recursive=True)
    observer.start()
    try:
        serve()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

