const filenames = [
    "2c32c35da827fad015c4664c699edd07.webp",
    "7692ca2a02e9f6c6e6dbfb4d5ea1b073.webp",
    "838343ddbe7b4fe946152e3c0cd552d9.webp",
    "9140b5aa24b8474c8870bd70017e24f3.webp",
    "98_9j3cdC1w.webp",
    "9KxPXaSBW9Q.webp",
    "9eO6maQiFGo.webp",
    "9fbdd26407902676b370d3efb789dde9.webp",
    "mount.jpeg",
];

function createElementFromHTML(htmlString) {
    var div = document.createElement('div');
    div.innerHTML = htmlString.trim();
  
    // Change this to div.childNodes to support multiple top-level nodes.
    return div.firstChild;
  }

const files_elem = document.getElementById("files");

filenames.forEach(name => {
    let html = `<div class="file image" onclick="open_image(this.id);" id="img_${name}" style="background-image: url(assets/images/fileimg/${name});"><div class="content"><p class="filename">${name}</p></div></div>`;
    console.log(html)
    files_elem.appendChild(createElementFromHTML(html));
});

let anim_going = false;
function userpanel_click() {
    if (anim_going)
        return;

    const dd = document.getElementById("user-dropdown");
    const close = document.getElementById("user-dropdown-close-area");
    
    if (dd.classList.contains("closing")) {
        dd.classList.remove("closing")
        dd.classList.remove("closed")
        close.classList.remove("closed")
    } else {
        dd.classList.add("closing")
        close.classList.add("closed")
        anim_going = true;
        setTimeout(() => {
            dd.classList.add("closed")
            anim_going = false;
        }, 100)
    }
}

function userpanel_close() {
    if (anim_going)
        return;

    userpanel_click();
}
