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
        el.src = `/api/images/${ava}`;
    }
}

function load_images() {
    let promises = []
    let elems = document.getElementsByClassName('img-load-assist');
    for (let i = 0; i < elems.length; i++) {
        let el = elems[i];

        promises += get_request(el.src)
            .then(responce => responce.blob())
            .then(images => {
                let outside = URL.createObjectURL(images);
                el.src = outside;
            });
    }

    let bg_elems = document.getElementsByClassName('bg-load-assist');
    for (let i = 0; i < bg_elems.length; i++) {
        let el = bg_elems[i];
        console.log("CUM", el.style.backgroundImage.slice(5, -2))
        promises += get_request(el.style.backgroundImage.slice(5, -2))
            .then(responce => responce.blob())
            .then(images => {
                console.log("BG", el, images);
                let outside = URL.createObjectURL(images);
                el.style.backgroundImage = `url(${outside})`;
            });
    }

    return Promise.all(promises);
}

function load_user_files() {
    return get_images()
        .then(data => {
            const files_elem = document.getElementById("files");
            console.log('GOT USER FILES: ', data);
            data.returned.forEach(name => {
                console.log('User image: ', name);
                let html = `<div class="file image bg-load-assist" onclick="open_image('/${name}');" style="background-image: url(/api/images/${name});"><div class="content"><p class="filename">${name}</p></div></div>`;

                console.log(`HTML: ${html}`);
                files_elem.appendChild(createElementFromHTML(html));
            });
        });
}

(() => {
    let a = update_username();
    let b = update_avatar();
    let c = load_user_files();

    Promise.all([a, b, c]).then(() => load_images());
})();