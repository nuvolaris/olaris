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

import os
import json
from pathlib import Path

MAINS = ["__main__.py",
         "index.js",
         "index.php",
         "main.go"]

SKIPDIR = ["virtualenv",
           "node_modules",
           "__pycache__"]

DEFAULT_REQ_GLOBS = ["packages/*/*/requirements.txt",
                     "packages/*/*/package.json",
                     "packages/*/*/composer.json",
                     "packages/*/*/go.mod"]

DEFAULT_MAIN_GLOBS = ["packages/*/*/index.js",
                      "packages/*/*/__main__.py",
                      "packages/*/*/index.php",
                      "packages/*/*/main.go"]

DEFAULT_SINGLES_GLOBS = ["packages/*/*.py",
                         "packages/*/*.js",
                         "packages/*/*.php",
                         "packages/*/*.go"]


def get_nuvolaris_config(key: str, default: list | str) -> (list | str):
    """Read package.json if exists and retrieve the required
    value for passed key (if defined)

    Args:
        key (str): the key of the parameter to retrieve
        default (list | str): the default value to return

    Returns:
        _type_: the list of values or the single string value.
        if not defined, the default value is returned
    """
    try:
        dir = os.environ.get("NUV_PWD", "/do_not_exists")
        file = f"{dir}/package.json"
        info = json.loads(Path(file).read_text())
        return info.get("nuvolaris", {}).get(key, default)
    except:
        return default
