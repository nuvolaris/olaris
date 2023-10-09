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
    const auth = process.env.AUTH
    const psqlAddr = `${process.env.APIHOST}/api/v1/web/whisk-system/nuv/psql`;

    command = process.argv[2]
    param = nuv.nuvExec("nuv","-base64","-d",process.argv[3])
    param = param.replace(/(\r\n|\n|\r)/gm,"")

    cmd = {}

    if ('desc' == command) {
        cmd['command']=`SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '${param}'`    
    }

    if ('sql' == command) {
        cmd['command']=param
    }

    console.log(JSON.stringify(cmd))
    
    let res = nuv.nuvExec("curl", `${psqlAddr}`,"-s","-H", `x-impersonate-auth: ${auth}`,"-H","Content-Type: application/json","-d", `${JSON.stringify(cmd)}`);
    console.log(res);

}
