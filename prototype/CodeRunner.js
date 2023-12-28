function base64ToBytes(base64) {
    // This function is copied from https://developer.mozilla.org/en-US/docs/Glossary/Base64
    const binString = atob(base64);
    return Uint8Array.from(binString, (m) => m.codePointAt(0));
}

function bytesToBase64(bytes) {
    return btoa(bytes);
}

let api_url = 'http://127.0.0.1:8000/api/v1';
let id = "42";
let enable_checking = false;

function setRunning() {
    let res_tag = document.getElementById("res");
    res_tag.innerHTML = "Код исполняется...";
}

function sendCode() {
    let code_ = editor.getValue();
    fetch(api_url + '/', {
        method: 'POST',
        body: JSON.stringify({
            code: bytesToBase64(code_), 
        }),
        headers: {
            'Content-Type': 'application/json; charset=UTF-8', 
            'Access-Control-Request-Method': 'POST'
        }
    }).then((response) => response.json())
      .then((json) => { id = json["id"]; setRunning(); enable_checking = true; });
}

setInterval(() => {
    if (enable_checking) {
        fetch(api_url + '/' + id, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
                'Access-Control-Request-Method': 'GET'
            }
        }).then((response) => response.json())
          .then((json) => {
            if (json["done"]) {
                let res_tag = document.getElementById("res");
                res_tag.innerHTML = json["html"];
                enable_checking = false;
                setupLists();
            }
          });
    }
}, 500);
