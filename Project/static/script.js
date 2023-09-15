document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var login = document.getElementById('login').value;
    var password = document.getElementById('password').value;
    var serverIp = document.getElementById('serverIp').value;

    fetch(serverIp + '/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            login: login,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status != 'ok') {
            alert('Failed: ' + data.status);
        } else {
            document.getElementById('authToken').value = data.token;
            alert('Status: ' + data.status);
        }
    });
});

document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var login = document.getElementById('reg_login').value;
    var password = document.getElementById('reg_password').value;
    var serverIp = document.getElementById('serverIp').value;

    fetch(serverIp + '/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            login: login,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
            alert('Status: ' + data.status);
    });
});

document.getElementById('sendForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var file = document.getElementById('filePicker').files[0];
    var filename = document.getElementById('fileName').value;
    var authToken = document.getElementById('authToken').value;
    var serverIp = document.getElementById('serverIp').value;

    var formData = new FormData();
    formData.append('token', authToken);
    formData.append('file', file);
    formData.append('filename', filename);

    fetch(serverIp + '/api/upload_file', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + authToken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data);
    });
});
