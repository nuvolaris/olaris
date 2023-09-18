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

const checkMultiFileAction = (package, entry) => {
    const path = nuv.joinPath(package, entry);
    if (nuv.isDir(path)) {
        return { isDir: true, runtime: findRuntime(path) };
    }
    return { isDir: false, runtime: null };
};

const supportedRuntimes = [".js", ".py", ".go", ".java"];
const supportedRuntimesValues = {
    "main.js": "nodejs:default",
    "__main__.py": "python:default",
    "main.go": "go:default",
    "main.java": "java:default",
    "main.php": "php:default",
}
const isSupportedRuntime = (file) => supportedRuntimes.includes(nuv.fileExt(file));

const findRuntime = (folder) => {
    const files = nuv.readDir(folder);
    for (const file of files) {
        if (supportedRuntimesValues[file]) {
            return supportedRuntimesValues[file];
        }
    }
    return null;
};


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

    manifest = scanEnv(manifest);

    let manifestYaml = nuv.toYaml(manifest);

    const manifestPath = nuv.joinPath(process.env.NUV_TMP, "manifest.yaml");

    nuv.writeFile(manifestPath, manifestYaml);
    console.log("Manifest file generated.");
}

function scanEnv(manifest) {
    console.log('Adding secrets...');

    let config = nuv.nuvExec('-config', '-d');


    const lines = config.split('\n');
    lines.forEach(function (line) {
        const parts = line.split('=');
        if (parts.length == 2) {
            const key = parts[0];
            if (!key.startsWith('SECRET_')) {
                return;
            }

            for (const packageName in manifest.packages) {
                if (!manifest.packages[packageName].inputs) {
                    manifest.packages[packageName].inputs = {};
                }
                manifest.packages[packageName].inputs[key.toLowerCase()] = `$${key}`;
            }
        }
    });

    return manifest;
}

function scanPackages(path) {
    manifest = { packages: {} };
    const packagesPath = nuv.joinPath(path, '/packages');
    if (!nuv.exists(packagesPath)) {
        return manifest;
    }

    console.log('Scanning packages folder...');
    nuv.readDir(packagesPath).forEach(function (entry) {
        const packagePath = nuv.joinPath(packagesPath, entry);
        // if it's a directory, it's an ow package
        if (nuv.isDir(packagePath)) {
            // check we are not overwriting the default package
            if (entry != 'default' || (entry == 'default' && !manifest.packages['default'])) {
                manifest.packages[entry] = { actions: {} };
            }
            scanSinglePackage(manifest, packagePath);
        } else {// otherwise it could be a single file action in the default package
            if (isSupportedRuntime(entry)) {
                // add 'default' package if not present
                if (!manifest.packages['default']) {
                    manifest.packages['default'] = { actions: {} };
                }
                const actionName = getActionName(entry);
                manifest.packages['default'].actions[actionName] = { function: nuv.basePath(packagePath), web: true };
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

        const packageName = nuv.basePath(packagePath);
        const actionName = getActionName(entry);
        if (isSingleFileAction(packagePath, entry) && isSupportedRuntime(entry)) {
            // console.log(packageName + '/' + entry + ' is supported single file action');
            manifest.packages[packageName].actions[actionName] = { function: nuv.joinPath(packageName, entry), web: true };
            return;
        }

        let { isDir, runtime } = checkMultiFileAction(packagePath, entry);
        if (isDir && runtime) {
            // console.log(packageName + '/' + entry + ' is multi file action');
            let res = nuv.nuvExec('-zipf', nuv.joinPath(packagePath, entry));

            // nuv -zipf prints the path of the zip file to stdout
            // so if the result doesn't end with .zip\n, it's an error
            if (!res.endsWith('.zip\n')) {
                console.error("ZIP ERROR:", res)
                return;
            }

            const functionEntry = nuv.basePath(res.split(" ")[2]).trim();
            manifest.packages[packageName].actions[actionName] = {
                function: nuv.joinPath(packageName, functionEntry),
                runtime,
                web: true,
            };
        }
    });
}
