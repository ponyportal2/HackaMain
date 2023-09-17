function get_img_size(src) {
    const elem = document.getElementById('buffer-img');
    elem.src = src;
    return [elem.width, elem.height];
}


var zoom_state = {
    zoom: 1.0,
    x: 0,
    y: 0,
    img_w: 0,
    img_h: 0,
    src: '',
};

function update_zoom_pos(zoom_in, x, y) {
    zoom_state.zoom = zoom_in;
    zoom_state.x = x;
    zoom_state.y = y;
    
    let zoom_image = document.getElementById('zoom-popup-image');
    let ze = Math.pow(1.1, zoom_state.zoom);

    zoom_image.style.left = zoom_state.x * ze - zoom_state.img_w * ze / 2 + 'px';
    zoom_image.style.top = zoom_state.y * ze - zoom_state.img_h * ze / 2 + 'px';
    zoom_image.style.width = `${zoom_state.img_w * ze}px`;
    zoom_image.style.height = `${zoom_state.img_h * ze}px`;
}

function on_zoom(delta) {
    if (isNaN(delta))
        return;

    let new_zoom = zoom_state.zoom + delta / 50.;
    update_zoom_pos(new_zoom, zoom_state.x, zoom_state.y);
}

function close_image_zoom() {
    const elem = document.getElementById("zoom-popup");
    elem.classList.add('closed');
}

function open_image(elem) {
    // console.log(`Opening image ${elem.style.backgroundImage}`);
    const popup = document.getElementById("zoom-popup");
    popup.classList.remove('closed');
    
    const bgelem = document.getElementById("zoom-popup-image");
    // let url = `assets/images/fileimg/${img_name}`;
    update_zoom_pos(0.0, 0.0, 0.0)
    let url = elem.dataset.src;
    
    console.log('url: ', elem.dataset.src);
    if (url.startsWith('/api/thumbs'))
        url = url.slice('/api/thumbs'.length)
    
    bgelem.dataset.src = '/api/images' + encodeURIComponent(url);
    bgelem.classList.add('img-load-assist');
    load_images()
        .then(() => setTimeout(() => {
            console.log('hello');
            bgelem.style = null;
            console.log('test ', bgelem.width, bgelem.height);
            console.log(bgelem);
            let size = [bgelem.width, bgelem.height];
            zoom_state.img_w = size[0];
            zoom_state.img_h = size[1];
        
            zoom_state.src = elem.dataset.src;
        
            update_zoom_pos(0.0, 0.0, 0.0)
        }, 200))

}

let zoom_drag = document.getElementById('zoom-popup-drag');

zoom_drag.addEventListener("wheel", (event) => {
    on_zoom(event.deltaY);
    event.stopPropagation();
    event.preventDefault();
}, {passive: false});

function onMouseMove(event) {
    if (isNaN(event.movementX) || isNaN(event.movementY))
        return;

    let ze = Math.pow(1.1, zoom_state.zoom);
    update_zoom_pos(zoom_state.zoom, zoom_state.x + event.movementX / ze, zoom_state.y + event.movementY / ze);
}

zoom_drag.onmousedown = function(event) {
    document.addEventListener('mousemove', onMouseMove);

    zoom_drag.onmouseup = function() {
      document.removeEventListener('mousemove', onMouseMove);
      zoom_drag.onmouseup = null;
    };
  
};

function delete_image_zoom() {
    // zoom_state.src.slice('/api/images/'.length)
    delete_file(zoom_state.src.slice('/api/images/'.length))
    .then(() => location.reload());
}

function trigger_set_avatar() {
    set_avatar(zoom_state.src.slice('/api/images/'.length))
    .then(() => location.reload());
}