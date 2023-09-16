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

function get_request(url) {
    return fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + get_auth_token(),
        },
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

async function get_username(token) {
    return json_request('/api/verify_token', { token: token })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        return (data.status == 'valid') ? data.user : null;
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

async function get_avatar() {
    return json_request('/api/get_avatar_pic', { token: get_auth_token() })
    .then(response => response.json())
    .then(data => data.returned == 'ur dumb' ? null : data.returned);
}

async function set_avatar(name) {
    return json_request('/api/set_avatar_pic', { token: get_auth_token(), filename: name })
    .then(response => response.json())
}


async function get_images() {
    return json_request('/api/get_all_files/', { token: get_auth_token(), pattern: '*' })
    .then(response => response.json());
}

async function get_images_for_album(album) {
    return json_request('/api/get_all_files/', { 
        token: get_auth_token(), 
        pattern: `${album}/*` 
    })
    .then(response => response.json());
}

async function create_folder(name) {
    return json_request('/api/create_folder/', { 
        token: get_auth_token(), 
        folder: name, 
    })
    .then(response => response.json());
}

async function delete_folder(name) {
    return json_request('/api/delete_folder/', { 
        token: get_auth_token(), 
        folder: name, 
    })
    .then(response => response.json());
}

async function get_folders() {
    return json_request('/api/get_all_folders/', { token: get_auth_token(), pattern: '*' })
    .then(response => response.json());
}

async function delete_file(file) {
    return json_request('/api/del_file/', { token: get_auth_token(), filename: file })
    .then(response => response.json());
}