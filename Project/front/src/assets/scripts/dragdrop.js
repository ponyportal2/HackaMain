const files_input = document.getElementById('files_input');

function dropHandler(ev) {
  console.log("File(s) dropped");

  const dataTransfer = new DataTransfer();

  for (let i = 0; i < files_input.files.length; i++)
      dataTransfer.items.add(files_input.files[i]);

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();

  if (ev.dataTransfer.items) {
    // Use DataTransferItemList interface to access the file(s)
    [...ev.dataTransfer.items].forEach((item, i) => {
      // If dropped items aren't files, reject them
      if (item.kind === "file") {
        const file = item.getAsFile();
      //   files_input.files.append(file);
      dataTransfer.items.add(file);
        console.log(`… file[${i}].name = ${file.name}`);
      }
    });
  } else {
    // Use DataTransfer interface to access the file(s)
    [...ev.dataTransfer.files].forEach((file, i) => {
      // .append(file);
      dataTransfer.items.add(file);
      console.log(`… file[${i}].name = ${file.name}`);
    });
  }

  files_input.files = dataTransfer.files;

  if (files_input.files.length > 0)
      document.getElementById('drop-area').classList.add('accepted');
}

function dragOverHandler(ev) {
  console.log("File(s) in drop zone");

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();
}

function send_files(ev) {
  ev.preventDefault();

  document.getElementById('drop-area').classList.add('loading');

  for (let i = 0; i < files_input.files.length; i++) {
      console.log("Send: ", files_input.files[i].name);
      let file = files_input.files[i];
      let formData = new FormData();
      formData.append('file', file);
      formData.append('filename', file.name);
      formData.append('token', get_auth_token());

      fetch(get_server_ip() + '/api/upload_file', {
          method: 'POST',
          headers: { 'Authorization': 'Bearer ' + get_auth_token() },
          body: formData
      })
      .then(response => response.json())
      .then(data => {
          alert(data);
          console.log(data);
      });
  }


  document.getElementById('drop-area').classList.add('remove');
}

/*
let submit_form = document.getElementById('sendForm');
if (submit_form)
submit_form.addEventListener('submit', function(e) {
    e.preventDefault();

    var file = document.getElementById('filePicker').files[0];
    var filename = document.getElementById('fileName').value;
    var authToken = document.getElementById('authToken').value;
    var serverIp = document.getElementById('serverIp').value;
});*/
