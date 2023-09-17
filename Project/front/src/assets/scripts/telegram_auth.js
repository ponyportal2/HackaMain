function telegram_popup_close() {
    document.getElementById('telegram-auth-popup').classList.add('closed');
}
function telegram_popup_open() {
    document.getElementById('telegram-auth-popup').classList.remove('closed');
}

function telegram_request_code() {
    api_request_telegram_code()
        .then(data => {
            if (data.status.length != 6) {
                alert('Failed to request for telegram authentication');
                console.log(data);
            } else {
                let str = '';
                for (let i = 0; i < data.status.length; i++) {
                    str += `${data.status[i]} `;
                }
                document.getElementById('telegram-code-placeholder').innerHTML = str;
            }
        })