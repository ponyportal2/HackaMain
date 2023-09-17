const album_name_els = document.getElementsByClassName('album-name');
let global_album_name;

(() => {
    const queryString = window.location.search;
    console.log(queryString);
    // ?product=shirt&color=blue&newuser&size=m
    const urlParams = new URLSearchParams(queryString);
    
    global_album_name = urlParams.get('name');
    dragdrop_send_prefix = global_album_name + '/';
})();

for (let i = 0; i < album_name_els.length; i++) {
    let item = album_name_els[i];
    item.innerHTML = global_album_name;
    console.log(item);
}

function trigger_delete_album() {
    delete_folder(global_album_name)
    .then(() => location.assign(`/static/app/index.html`));
}