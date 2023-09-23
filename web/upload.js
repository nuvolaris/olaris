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

// *** Main ***
main();

function main() {
    let path = process.argv[2];
    let quiet = process.argv[3];

    let minioKey = `${process.env.NUVUSER.toUpperCase()}_SECRET_MINIO`;
    if (process.env.NUVUSER == 'nuvolaris') {
        minioKey = "SECRET_MINIO_NUVOLARIS"
    }

    const minioAuth = process.env[minioKey];
    const uploadAddr = `${process.env.APIHOST}/api/v1/web/whisk-system/nuv/upload/${process.env.NUVUSER}`;

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


            let res = nuv.nuvExec("curl", "-X", "PUT", "-T", file, "-H", `minioauth: ${minioAuth}`, `${uploadAddr}/${fileAddr}`);
            if (!quiet) {
                console.log(res);
            }
        }
    })
}
