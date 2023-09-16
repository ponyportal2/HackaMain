function get_auth_token() {
    return localStorage.getItem('auth_token');
}

function set_auth_token(token) {
    localStorage.setItem('auth_token', token);
}

function get_server_ip() {
    return 'http://localhost:5000'
}