function open_album(name) {
    location.assign(`/album.html?name=${encodeURI(name)}`);
}

function on_album_create() {
    location.assign(`/album.html?name=123`);
}