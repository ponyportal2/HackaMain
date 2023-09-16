const PREFIX = '/static/app';

function json_request(url, req) {
    return fetch(get_server_ip() + url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + get_auth_token(),
        },
        body: JSON.stringify(req)
    })
}

async function verify_token(token) {
    return json_request('/api/verify_token', { token: token })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        return data.status == 'valid';
    });
}

async function sign_in(login, password) {
    return json_request('/api/login', { login: login, password: password })
    .then(response => response.json())
    .then(data => {
        if (data.status == 'ok') {
            return { token: data.token };
        } else {
            return { token: null };
        }
    });
}

async function sign_up(login, password) {
    return json_request('/api/register', { login: login, password: password })
    .then(response => response.json())
    .then(data => {
        if (data.status == 'success') {
            return { ok: true };
        } else {
            return { ok: false };
        }
    });
}

async function logout() {
    return json_request('/api/logout', { token: get_auth_token() })
    .then(response => response.json())
    .then(data => {});
}