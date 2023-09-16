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
        console.log(data);
    });
});

document.getElementById('moveForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var authToken = document.getElementById('authToken').value;
    var serverIp = document.getElementById('serverIp').value;

    fetch(serverIp + '/api/mv_file', {
        method: 'POST',
        headers: { 
            'Authorization': 'Bearer ' + authToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            filename_from: document.getElementById('mv_from').value,
            filename_into: document.getElementById('mv_to').value, 
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status);
        console.log(data);
    });
});


document.getElementById('verifyForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var authToken = document.getElementById('authToken').value;
    var serverIp = document.getElementById('serverIp').value;

    console.log(serverIp + '/api/verify_token');
    fetch(serverIp + '/api/verify_token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: authToken,
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status);
        console.log(data);
    });
});

document.getElementById('deleteForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var authToken = document.getElementById('authToken').value;
    var serverIp = document.getElementById('serverIp').value;

    fetch(serverIp + '/api/del_file', {
        method: 'POST',
        headers: { 
            'Authorization': 'Bearer ' + authToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: authToken,
            filename: document.getElementById('del_name').value,
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status);
        console.log(data);
    });
});

document.getElementById('getallForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var authToken = document.getElementById('authToken').value;
    var serverIp = document.getElementById('serverIp').value;

    fetch(serverIp + '/api/get_all_files', {
        method: 'POST',
        headers: { 
            'Authorization': 'Bearer ' + authToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            token: authToken,
            pattern: document.getElementById('get_all_pattern').value,
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status);
        console.log(data);
    });
});

document.getElementById('getallfoldersForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var authToken = document.getElementById('authToken').value;
    var serverIp = document.getElementById('serverIp').value;

    fetch(serverIp + '/api/get_all_folders', {
        method: 'POST',
        headers: { 
            'Authorization': 'Bearer ' + authToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            token: authToken,
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status);
        console.log(data);
    });
});


document.getElementById('logOutForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var authToken = document.getElementById('authToken').value;
    var serverIp = document.getElementById('serverIp').value;

    fetch(serverIp + '/api/logout', {
        method: 'POST',
        headers: { 
            'Authorization': 'Bearer ' + authToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            token: authToken,
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status);
        console.log(data);
    });
});


document.getElementById('get_avatar').addEventListener('submit', function(e) {
    e.preventDefault();
    var authToken = document.getElementById('authToken').value;
    var serverIp = document.getElementById('serverIp').value;

    fetch(serverIp + '/api/get_avatar_pic', {
        method: 'POST',
        headers: { 
            'Authorization': 'Bearer ' + authToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            token: authToken,
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status);
        console.log(data);
    });
});


document.getElementById('set_avatar').addEventListener('submit', function(e) {
    e.preventDefault();
    var authToken = document.getElementById('authToken').value;
    var serverIp = document.getElementById('serverIp').value;

    fetch(serverIp + '/api/set_avatar_pic', {
        method: 'POST',
        headers: { 
            'Authorization': 'Bearer ' + authToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            token: authToken,
            filename: document.getElementById('set_avatar_name').value
            
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status);
        console.log(data);
    });
});