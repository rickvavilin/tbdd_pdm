var api_base_url='/api';

function api_url(url_elements, parameters={}){
    let url = api_base_url+'/'+url_elements.join('/');

    if (parameters=!{}){
        let param_pairs = [];
        for (let i in parameters){
            param_pairs.push(i+'='+parameters[i])
        }
        url = url+'?'+param_pairs.join('&')
    }
    return url
}

function api_fetch(url_elements, options, parameters={}){
    options.credentials = 'same-origin';
    return fetch(api_url(url_elements, parameters), options)
}

function api_fetch_json(url_elements, options, parameters={}){
    return api_fetch(url_elements, options, parameters).then(
        (response) => {
            if ((response.status>=200) && (response.status<300)) {
                return response.json()
            } else {
                throw 'FetchError'
            }
        }
    )
}

function api_post_json(url_elements, data, options, parameters={}){
    options.method = 'POST';
    options.headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };
    options.body = JSON.stringify(data);
    return api_fetch_json(url_elements, options, parameters)
}

function api_delete_json(url_elements, options, parameters={}){
    options.method = 'DELETE';
    options.headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };
    return api_fetch_json(url_elements, options, parameters)
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
        return api_post_json(['auth', 'login'],{
                        'login': login,
                        'password_hash': password_hash
                    },{});
    });
}

function api_loggedin(){
    return api_fetch_json(['auth', 'loggedin'], {})
}

function api_logout(){
    return api_fetch_json(['auth', 'logout'], {})
}