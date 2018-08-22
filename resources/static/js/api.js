var api_base_url='/api';

function api_url(url_elements){
    return api_base_url+'/'+url_elements.join('/');
}

function api_fetch(url_elements, options){
    options.credentials = 'same-origin';
    return fetch(api_url(url_elements), options)
}

function api_fetch_json(url_elements, options){
    return api_fetch(url_elements, options).then(
        (response) => {
            if ((response.status>=200) && (response.status<300)) {
                return response.json()
            } else {
                throw 'FetchError'
            }
        }
    )
}

function api_post_json(url_elements, options){
    options.method = 'POST';
    options.headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };
    return api_fetch_json(url_elements, options)
}

async function _sha256(message) {
    // encode as UTF-8
    const msgBuffer = new TextEncoder('utf-8').encode(message);

    // hash the message
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);

    // convert ArrayBuffer to Array
    const hashArray = Array.from(new Uint8Array(hashBuffer));

    // convert bytes to hex string
    const hashHex = hashArray.map(b => ('00' + b.toString(16)).slice(-2)).join('');
    return hashHex;
}

function api_login(login, password){
    return _sha256(password).then((password_hash)=>{
        return api_post_json(['auth', 'login'], {
                body: JSON.stringify(
                    {
                        'login': login,
                        'password_hash': password_hash
                    }
                )
            })
    });
}

function api_loggedin(){
    return api_fetch_json(['auth', 'loggedin'], {})
}

function api_logout(){
    return api_fetch_json(['auth', 'logout'], {})
}