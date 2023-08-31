// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.


// nuv functions:
// scan(root, functions): walks the substree starting in root, execute a function (returning a string) for each folder
// readfile(file): read an entire file
// writefile(file, body): write an entirefile
// readdir(folder): read a folder and return an array of filenames
// toyaml(object): encode in yaml a js object
// fromyaml(string): decode a string assuming it is yaml in a js object

const nuv = require('nuv');

let path = process.argv[2];

let manifest = {};

manifest = scanPackages();
scanWeb();


function scanPackages(manifest) {
    manifest = { packages: {} };
    console.log('Scanning packages folder...');
    const packagesFolderPath = path + '/packages';
    if (!nuv.exists(packagesFolderPath)) {
        console.log('Packages folder not found');
        return;
    }

    nuv.readDir(packagesFolderPath).forEach(function (entry) {
        let isPackage = nuv.isDir(nuv.joinPath(packagesFolderPath, entry));
        if (isPackage) {
            // check we are not overwriting the default package
            if (entry != 'default' || (entry == 'default' && !manifest.packages['default'])) {
                manifest.packages[entry] = { actions: {} };
            }
        } else {
            if (isSupportedRuntime(entry)) {
                const actionName = getActionName(entry);
                // add 'default' package if not present
                if (!manifest.packages['default']) {
                    manifest.packages['default'] = { actions: {} };
                }
                console.log('Adding action ' + actionName + ' to package default');
                manifest.packages['default'].actions[actionName] = { function: entry };
            }
        }
    });
    console.log('Packages scanned');
    console.log('Manifest: ' + JSON.stringify(manifest, null, 2));
    return manifest;
}


function scanWeb() {
    console.log("Scanning web folder...");
    const webFolderPath = path + '/web';
    if (!nuv.exists(webFolderPath)) {
        console.log('Web folder not found');
        return;
    }
    console.log("Web folder scanned");
}

function isSupportedRuntime(file) {
    const supportedRuntimes = [".js", ".py", ".go", ".java"];
    let ext = nuv.fileExt(file)
    let b = supportedRuntimes.includes(ext);
    return b;
}

function getActionName(path) {
    const basePath = nuv.basePath(path);
    const ext = nuv.fileExt(basePath)
    return basePath.substring(0, basePath.length - ext.length);
}