function trigger_signup(event) {
    event.preventDefault();

    let login = document.getElementById('reg_login').value;
    let password = document.getElementById('reg_password').value;

    sign_up(login, password)
        .then(result => {
            if (result.ok) {
                sign_in(login, password)
                    .then(result => {
                        set_auth_token(result.token);
                        location.assign(`${PREFIX}/index.html`);
                    });
            } else {
                alert('Failed to sign up!');
            }
        });
}
function trigger_signin(event) {
    event.preventDefault();

    let login = document.getElementById('login').value;
    let password = document.getElementById('password').value;

    sign_in(login, password)
    .then(result => {
        if (result.token) {
            set_auth_token(result.token);
            location.assign(`${PREFIX}/index.html`);
        } else {
            alert('Failed to sign in!');
        }
    });
}