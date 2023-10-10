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

function decode_and_norm(value) {
    decoded = nuv.nuvExec("nuv","-base64","-d",value)
    return decoded.replace(/(\r\n|\n|\r)/gm,"")
}

function main() {
    const auth = process.env.AUTHB64
    const minioAddr = `${process.env.APIHOST}/api/v1/web/whisk-system/nuv/minio`;
    const uploadAddr = `${process.env.APIHOST}/api/v1/web/whisk-system/nuv/devel_upload`;
    const downloadAddr = `${process.env.APIHOST}/api/v1/web/whisk-system/nuv/devel_download`;

    command = process.argv[2]

    cmd = {}

    if ('ls' == command) {
        cmd['command']="ls"    
    }

    if ('lsb' == command) {
        bucket = decode_and_norm(process.argv[3])
        cmd['command']="ls"
        cmd['args']=[bucket]
    }

    if ('rm' == command) {
        bucket = decode_and_norm(process.argv[3])
        file = decode_and_norm(process.argv[4])
        cmd['command']="rm"
        cmd['args']=[bucket,file]
    } 
    
    if ('mv' == command) {
        bucket = decode_and_norm(process.argv[3])
        file = decode_and_norm(process.argv[4])
        dest_bucket = decode_and_norm(process.argv[5])
        dest_file = decode_and_norm(process.argv[6])

        cmd['command']="mv"
        cmd['args']=[bucket,file,dest_bucket,dest_file]
    }  
    
    if ('cp' == command) {
        bucket = decode_and_norm(process.argv[3])
        file = decode_and_norm(process.argv[4])
        dest_bucket = decode_and_norm(process.argv[5])
        dest_file = decode_and_norm(process.argv[6])

        cmd['command']="cp"
        cmd['args']=[bucket,file,dest_bucket,dest_file]
    }  
    
    if ('put' == command) {
        localfile = decode_and_norm(process.argv[3])
        bucket = decode_and_norm(process.argv[4])
        file = decode_and_norm(process.argv[5])
    }
    
    if ('get' == command) {        
        bucket = decode_and_norm(process.argv[3])
        file = decode_and_norm(process.argv[4])
    }

    if ( command != "put"  && command != "get" ) {
        let res = nuv.nuvExec("curl", `${minioAddr}`,"-s","-H", `x-impersonate-auth: ${auth}`,"-H","Content-Type: application/json","-d", `${JSON.stringify(cmd)}`)
        console.log(res);         
        return
    } 
    
    if ( command == "put" ) {
        if ( nuv.exists(localfile) ) {
            let res = nuv.nuvExec("curl", `${uploadAddr}/${bucket}/${file}`,"-s","-X", "PUT", "-T",`${localfile}`,"-H", `x-impersonate-auth: ${auth}`)
            console.log(res);    
        } else {
            console.log(`invalid filename ${localfile} provided`)
        }
    }

    if ( command == "get" ) {
        let split = file.split("/")
        let output_file = split[split.length -1]
        console.log(output_file)
        let res = nuv.nuvExec("curl", `${downloadAddr}/${bucket}/${file}`,"-v","-H", `x-impersonate-auth: ${auth}`, "-o", `${output_file}`)
        console.log(res);
    }


}
