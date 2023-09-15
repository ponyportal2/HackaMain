function get_img_size(src) {
    const elem = document.getElementById('buffer-img');
    elem.src = src;
    return [elem.width, elem.height];
}


let zoom = 1.0;

let zoom_img_x = 0.0;
let zoom_img_y = 0.0;

let img_w = 0;
let img_h = 0;

function update_zoom_pos(zoom_in, x, y) {
    zoom = zoom_in;
    zoom_img_x = x;
    zoom_img_y = y;
    // zoom_drag.style.left = pageX - zoom_drag.offsetWidth / 2 + 'px';
    // zoom_drag.style.top = pageY - zoom_drag.offsetHeight / 2 + 'px';
    let zoom_image = document.getElementById('zoom-popup-image');
    const ze = Math.pow(1.1, zoom);
    // console.log("image size: ", img_w, img_h, zoom_img_x, zoom_img_y, ze);
    zoom_image.style.backgroundPositionX = zoom_img_x - img_w*ze + 'px';
    zoom_image.style.backgroundPositionY = zoom_img_y - img_h*ze + 'px';
    zoom_image.style.backgroundSize = `${ze * 100}%`;
}

function on_zoom(delta) {
    update_zoom_pos(zoom + delta / 50., zoom_img_x, zoom_img_y);
}

function close_image_zoom() {
    const elem = document.getElementById("zoom-popup");
    elem.classList.add('closed');
}

function open_image(id) {
    const img_name = id.substring("img_".length);
    
    const elem = document.getElementById("zoom-popup");
    elem.classList.remove('closed');
    
    const bgelem = document.getElementById("zoom-popup-image");
    let url = `/assets/images/fileimg/${img_name}`;
    bgelem.style.backgroundImage = `url(${url})`
    let size = get_img_size(url);
    img_w = size[0];
    img_h = size[1];
    update_zoom_pos(0.0, document.width / 2, document.height / 2)
}

let zoom_drag = document.getElementById('zoom-popup-drag');

zoom_drag.addEventListener("wheel", (event) => {
    on_zoom(event.deltaY);
    event.stopPropagation();
    event.preventDefault();
}, {passive: false});

function onMouseMove(event) {
    update_zoom_pos(zoom, zoom_img_x + event.movementX, zoom_img_y + event.movementY)
}

zoom_drag.onmousedown = function(event) {
    document.addEventListener('mousemove', onMouseMove);

    zoom_drag.onmouseup = function() {
      document.removeEventListener('mousemove', onMouseMove);
      zoom_drag.onmouseup = null;
    };
  
  };
  