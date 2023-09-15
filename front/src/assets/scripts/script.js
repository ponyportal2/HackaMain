const filenames = [
    "2c32c35da827fad015c4664c699edd07.webp",
    "7692ca2a02e9f6c6e6dbfb4d5ea1b073.webp",
    "838343ddbe7b4fe946152e3c0cd552d9.webp",
    "9140b5aa24b8474c8870bd70017e24f3.webp",
    "98_9j3cdC1w.webp",
    "9KxPXaSBW9Q.webp",
    "9eO6maQiFGo.webp",
    "9fbdd26407902676b370d3efb789dde9.webp",
];

function createElementFromHTML(htmlString) {
    var div = document.createElement('div');
    div.innerHTML = htmlString.trim();
  
    // Change this to div.childNodes to support multiple top-level nodes.
    return div.firstChild;
  }

const files_elem = document.getElementById("files");

filenames.forEach(name => {
    let html = `<div class="file image" style="background-image: url(assets/images/fileimg/${name});"><div class="content"><p class="filename">${name}</p></div></div>`;
    console.log(html)
    files_elem.appendChild(createElementFromHTML(html));
});

function userpanel_click() {
    const elem = document.getElementById("user-dropdown");
    
    if (elem.style.display == 'flex')
        elem.style.display = 'none';
    else
        elem.style.display = 'flex';
}