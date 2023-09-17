function get_auth_token() {
    return localStorage.getItem('auth_token');
}

function set_auth_token(token) {
    localStorage.setItem('auth_token', token);
}

function get_server_ip() {
    return 'http://92.51.47.120:5000'
}
