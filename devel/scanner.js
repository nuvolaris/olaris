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

const nuv = require('nuv');

// *** Utility functions ***

const isSingleFileAction = (package, entry) => !nuv.isDir(nuv.joinPath(package, entry));

// TODO: check for package.json, go.mod, requirements.txt, pom.xml
const isMultiFileAction = (package, entry) => nuv.isDir(nuv.joinPath(package, entry));

const supportedRuntimes = [".js", ".py", ".go", ".java"];
const isSupportedRuntime = (file) => supportedRuntimes.includes(nuv.fileExt(file));

// Get the action name from the file name: "/path/to/action.js" -> "action"
function getActionName(path) {
    const basePath = nuv.basePath(path);
    const ext = nuv.fileExt(basePath)
    return basePath.substring(0, basePath.length - ext.length);
}

// *** Main ***
main();

function main() {
    let path = process.argv[2];
    let manifest = scanPackages(path);
    scanWeb(path);
    let manifestYaml = nuv.toYaml(manifest);
    nuv.writeFile(nuv.joinPath(path, "manifest.yml"), manifestYaml);
    console.log("Manifest file written at " + nuv.joinPath(path, "manifest.yml"));
}

function scanPackages(path) {
    manifest = { packages: {} };
    const packagesFolderPath = path + '/packages';
    if (!nuv.exists(packagesFolderPath)) {
        return manifest;
    }

    console.log('Scanning packages folder...');
    nuv.readDir(packagesFolderPath).forEach(function (entry) {
        const packagePath = nuv.joinPath(packagesFolderPath, entry);
        // if it's a directory, it's an ow package
        if (nuv.isDir(packagePath)) {
            // check we are not overwriting the default package
            if (entry != 'default' || (entry == 'default' && !manifest.packages['default'])) {
                manifest.packages[entry] = { actions: {} };
            }
            scanSinglePackage(manifest, packagePath);
        } else {// otherwise it could be a single file action in the default package
            if (isSupportedRuntime(entry)) {
                // console.log(entry + ' is supported single file action in default package');
                const actionName = getActionName(entry);
                // add 'default' package if not present
                if (!manifest.packages['default']) {
                    manifest.packages['default'] = { actions: {} };
                }
                manifest.packages['default'].actions[actionName] = { function: entry, web: true };
            }
        }
    });
    console.log('Packages scanned');
    return manifest;
}

function scanSinglePackage(manifest, packagePath) {
    const packageName = nuv.basePath(packagePath);
    // console.log('Scanning package ' + packageName);
    nuv.readDir(packagePath).forEach(function (entry) {
        // console.log('Scanning ' + packageName + '/' + entry);
        // if the ext is .zip it's probably an old zip action
        if (nuv.fileExt(entry) == '.zip') {
            return;
        }

        const actionName = getActionName(entry);
        let functionEntry = nuv.joinPath(packageName, entry);
        let err = false;

        if (isSingleFileAction(packagePath, entry) && isSupportedRuntime(entry)) {
            // console.log(packageName + '/' + entry + ' is supported single file action');
            const actionName = getActionName(entry);
        } else if (isMultiFileAction(packagePath, entry)) {
            // console.log(packageName + '/' + entry + ' is multi file action');
            let res = nuv.nuvExec('-zipf', nuv.joinPath(packagePath, entry));

            // nuv -zipf prints the path of the zip file to stdout
            // so if the result doesn't end with .zip\n, it's an error
            if (!res.endsWith('.zip\n')) {
                console.error("ZIP ERROR:", res)
                err = true;
            }

            functionEntry = nuv.basePath(res.split(" ")[2]).trim();
        }

        if (!err) {
            manifest.packages[packageName].actions[actionName] = { function: functionEntry, web: true };
        }
    });
}

function scanWeb(path) {
    const webFolderPath = path + '/web';
    if (!nuv.exists(webFolderPath)) {
        console.log('Web folder not found');
        return;
    }
    // console.log("Scanning web folder...");
    // console.log("TODO: implement web folder scanning");
}

