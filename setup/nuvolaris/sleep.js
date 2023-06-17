function sleep(timeout) {
    return new Promise(resolve => setTimeout(resolve, timeout*1000))
}
async function main(args) {
    let timeout = args.sleep || "10"
    console.log("waiting "+timeout)
    await sleep(parseInt(timeout))
    return {
        "body": "waited "+timeout+" seconds (use SLEEP=<seconds>)"
    }
}