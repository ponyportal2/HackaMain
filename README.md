# How to: Build web client

Inside the `Project` folder, run `make web_client`. It will build web client and include it into the server (`/static/app` url). Then it will be available on the server via: `<server-ip/static/app/index.html`

You can also use it locally or in any location, as long as the files structure remains.

Warning: currently, server ip is set directly in `Project/front/src/assets/scripts/get_auth_token.js`, function `get_server_ip`. TODO: Make config?

# How to: Build Electron client (UNTESTED)

Inside the `Project` folder, run `make electron client`. It will build electron app from the project.

You can also use it locally or in any location, as long as the files structure remains.

# How to: Run server

Inside the `Project` folder, run `make req`, then run `make`. It also might lack required python libraries, then you will need to `pip install` those.