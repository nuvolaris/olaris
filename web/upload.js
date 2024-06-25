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

const contentActionAddr = `${process.env.APIHOST}/api/v1/web/whisk-system/nuv/devel_upload/${process.env.MINIO_BUCKET_STATIC}`;

// *** Main ***
main();

function main() {
    let path = process.argv[2];
    let verboseParam = process.argv[3];
    let cleanParam = process.argv[4];

    let verbose = extractBoolFromParam(verboseParam);
    let clean = extractBoolFromParam(cleanParam);


    const minioAuth = process.env.AUTHB64

    const pathFoundAsDir = nuv.isDir(path);
    if (!pathFoundAsDir) {
        console.log(`ERROR: ${path} is not a directory`);
        return;
    }

    nuv.scan(path, (folder) => {
        const entries = nuv.readDir(folder);

        for (const entry of entries) {
            if (nuv.isDir(nuv.joinPath(folder, entry))) {
                continue;
            }

            const file = nuv.joinPath(folder, entry);
            // remove path from folder and prepend the result to entry
            let fileAddr = folder.replace(path, "") + "/" + entry;
            if (fileAddr.startsWith("/")) {
                fileAddr = fileAddr.substring(1);
            }

            if (clean) {
                deleteContent(minioAuth, fileAddr, verbose);
            } else {
                uploadContent(file, minioAuth, fileAddr, verbose);
            }
        }
    })
}

function uploadContent(file, minioAuth, fileAddr, verbose) {
    console.log(`Uploading ${fileAddr}...`);
    let res = nuv.nuvExec("curl", "-s", "-X", "PUT", "-T", file, "-H", `x-impersonate-auth: ${minioAuth}`, `${contentActionAddr}/${fileAddr}`);
    if (verbose) {
        console.log(res);
    }
}

function deleteContent(minioAuth, fileAddr, verbose) {
    console.log(`Deleting ${fileAddr}...`);
    let res = nuv.nuvExec("curl", "-s", "-X", "DELETE", "-H", `x-impersonate-auth: ${minioAuth}`, `${contentActionAddr}/${fileAddr}`);
    if (verbose) {
        console.log(res);
    }
}

function extractBoolFromParam(param) {
    let verboseBool = param.split("=")[1];
    if (verboseBool === "true") {
        return true;
    }
    return false;
}

