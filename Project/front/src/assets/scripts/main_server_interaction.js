async function update_username() {
    let username = await get_username(get_auth_token());
    console.log("Got username: ", username);

    let elems = document.getElementsByClassName('user-name');
    for (let i = 0; i < elems.length; i++) {
        let el = elems[i];
        el.innerHTML = username;
    }
}

async function update_avatar() {
    let ava = await get_avatar();
    console.log("Got avatar: ", ava);

    let elems = document.getElementsByClassName('user-avatar');
    for (let i = 0; i < elems.length; i++) {
        let el = elems[i];
        if (ava) {
            el.dataset.src = `/api/images/${ava}`;
            el.classList.add('img-load-assist')
        } else {
            el.src = `/static/app/assets/images/user.webp`;
            el.classList.remove('img-load-assist')
        }
    }
}

function load_images() {
    let promises = []
    let elems = document.getElementsByClassName('img-load-assist');
    for (let i = 0; i < elems.length; i++) {
        let el = elems[i];
        promises += get_request(get_server_ip() + el.dataset.src)
            .then(responce => responce.blob())
            .then(images => {
                let outside = URL.createObjectURL(images);
                el.src = outside;
            });
    }

    let bg_elems = document.getElementsByClassName('bg-load-assist');
    for (let i = 0; i < bg_elems.length; i++) {
        let el = bg_elems[i];
        promises += get_request(get_server_ip() + el.dataset.src)
            .then(responce => responce.blob())
            .then(images => {
                let outside = URL.createObjectURL(images);
                el.style.backgroundImage = `url(${outside})`;
            });
    }

    return Promise.all(promises);
}

function load_user_files(album) {

    let images = album ? get_images_for_album(album) : get_images();

    return images
        .then(data => {
            const files_elem = document.getElementById("files");
            console.log('GOT USER FILES: ', data);
            data.returned.forEach(name => {
                let html = `<div class="file image bg-load-assist" onclick="open_image(this);" data-src="/api/images/${name}"><div class="content"><p class="filename">${name}</p></div></div>`;

                files_elem.appendChild(createElementFromHTML(html));
            });
        });
}

function load_user_albums() {
    return get_folders()
        .then(data => {
            const albums_elem = document.getElementById("albums");
            console.log('GOT USER FOLDERS: ', data);
            data.returned.forEach(name => {
                let html = `<div class="file album"><div class="content"><div class="folder-icon" onclick="open_album('${name}');"></div><span class="album-name">${name}</span></div></div>`;

                albums_elem.appendChild(createElementFromHTML(html));
            });
        });
}

function mservi_init() {
    let a = update_username();
    let b = update_avatar();
    let c = load_user_files();
    let d = load_user_albums();

    Promise.all([a, b, c, d]).then(() => load_images());
}

function mservi_init_album(name) {
    let a = update_username();
    let b = update_avatar();
    let c = load_user_files(name);

    Promise.all([a, b, c]).then(() => load_images());
}