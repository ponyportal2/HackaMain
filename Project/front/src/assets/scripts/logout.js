function trigger_logout(event) {
    event.preventDefault();

    logout()
        .then(() => location.reload());
}