// web/main.js

function handleClick(callback_name) {
    if (window.pywebview) {
        window.pywebview.api.on_pressed(callback_name).then(function(response) {
            console.log(response);
        }).catch(function(error) {
            console.error(error);
        });
    } else {
        console.error('pywebview is not defined');
    }
}

