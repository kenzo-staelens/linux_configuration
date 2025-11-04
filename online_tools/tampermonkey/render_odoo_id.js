// ==UserScript==
// @name         Render odoo ID
// @namespace    accomodata
// @version      2025-08-04
// @description  Render Taskid in odoo hotbar
// @author       You
// @match        https://*/*
// @match        http://*/*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        none
// ==/UserScript==

let trigger_counter = 0;
let found_odoo = false;
let trigger_interval = 10;

async function get_version_number(){
    let r = await fetch(`${document.location.protocol}//${document.location.host}/web/webclient/version_info`, {
        "credentials": "include",
        "headers": {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=4"
        },
        "referrer": `https://${document.location.host}/`,
        "body": "{}",
        "method": "POST",
        "mode": "cors"
    });

    let jsonval = await r.json()
    return jsonval.result.server_version_info[0]
}

function get_id_v_17(){
    let url = document.URL;
    if(url.includes('model=')){
        let res = url.match('(?:&|#)(?:active_|id)=([0-9]{5})');
        if(res && res.length>1){
            res = res[1];
            return res;
        }
        else return -1;
    }
    return -1;
}

function get_id_v_18(){
    let url = document.URL;
    let split = url.split('/')
    split = split[split.length-1];
    split = split.split('?')[0];
    return split;
}

function update_title(title, id){
    if(id==-1) return title;
    return id + ' - ' + document.title.split(' - ')[1];
}

function get_id(version){
    switch(version){
        case 17:
            return get_id_v_17();
        case 18:
            return get_id_v_18();
        default:
            return -1;
    }
}

(async function() {
    'use strict';
    let version = await get_version_number(); //undefined if error
    while(!document.title.includes(' - ')){
        await new Promise(r => setTimeout(r, 1000));
    }
    let id_title = document.title;
    let id = get_id(version);

    setInterval(()=>{
        id = get_id(version)
        id_title = update_title(document.title, id)
        document.title = id_title;
    },trigger_interval);
})();
