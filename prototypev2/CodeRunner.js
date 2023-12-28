function bytesToBase64(bytes) {
    return btoa(bytes);
}

let api_url = 'http://127.0.0.1:8000/api/v1';
let code_id = 42;
let enable_checking = false;

function setRunning() {
    let res_tag = document.getElementById("res");
    res_tag.innerHTML = "Код исполняется...";
}

function runCode() {
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
      .then((json) => { code_id = json["id"]; setRunning(); enable_checking = true; });
}

function stopCode() {
    let res_tag = document.getElementById("res");
    res_tag.innerHTML = "Код не запущен";
    enable_checking = false;
}

setInterval(() => {
    if (enable_checking) {
        fetch(api_url + '/' + code_id, {
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


