function open_album(name) {
    location.assign(`album.html?name=${encodeURI(name)}`);
}

function on_album_create() {
    create_folder('hello')
}

function open_create_album() {
  document.getElementById('create-album-popup')
  .classList.remove('closed');
}

function close_create_album() {
  document.getElementById('create-album-popup')
  .classList.add('closed');
}


function create_album(event) {
    event.preventDefault();
    let folder_name = document.getElementById('create-album-name').value.toString();

    console.log(folder_name.search('\\\/'), folder_name.search('\\\*'), folder_name.search('\\\:'), folder_name.search('\\\;'));
    if (folder_name.search('\\\/') >= 0 || folder_name.search('\\\*') >= 0 || folder_name.search('\\\:') >= 0 || folder_name.search('\\\;') >= 0) {
        alert('Invalid name');
        return;
    }

    create_folder(folder_name);
    location.reload();
}