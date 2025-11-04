// ==UserScript==
// @name         Goto Taskid
// @namespace    accomodata
// @version      2025-08-04
// @description  Hotkey to jump between tasks by id
// @author       You
// @match        https://*/*
// @match        http://*/*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        none
// ==/UserScript==



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

let onKeyDown = (e) => {

    /*
    0 = off
    1 = on
    keyCodeObject outputs the event object of the KeyEvent
    keyCode outputs the keyCode of the key thats been pressed
    */
    let log = {keyCodeObject: 0, keyCode: 0}


    let keyAlt = e.altKey;
    let keyCtrl = e.ctrlKey;
    let keyShift = e.shiftKey;

    if(log.keyCodeObject){console.log(e);}

    // https://unixpapa.com/js/key.html
    // get the code representation of the key pressed.
    let keyCode = e.which === 0 ? e.charCode : e.keyCode;

    if(log.keyCode){console.log(keyCode);}

    // match ';' key
    if (keyCode == 59 && keyCtrl){
        triggerNav();
    }
}

function get_host(){
    return `${document.location.protocol}//${document.location.host}`
}

function url_v_17(host, id){
    return `${host}/web#id=${id}&cids=1&action=2025&model=project.task&view_type=form`;
}

function url_v_18(host, id){
    return `${host}/my-tasks/${id}`
}

async function get_url(id){
    let host = get_host();
    let version = await get_version_number();
    switch(version){
        case 17:
            return url_v_17(host, id);
        case 18:
            return url_v_18(host, id)
    }
    return document.URL;
}

async function triggerNav(){
    let id = parseInt(prompt("TaskId"));
    if(id != NaN){
        window.location = await get_url(id);
    }
}

(function() {
    'use strict';
    document.addEventListener("keydown", onKeyDown);
})();
