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


function handleClickOnTap(callback_name, index) {
    if (window.pywebview) {
        window.pywebview.api.on_pressed(callback_name, index).then(function(response) {
            console.log(response);
        }).catch(function(error) {
            console.error(error);
        });
    } else {
        console.error('pywebview is not defined');
    }
}


function openDrawer() {
    var drawer = document.getElementById('drawer');
    drawer.classList.remove('drawer-closed');
    drawer.classList.add('drawer-open');
}

function closeDrawer() {
    var drawer = document.getElementById('drawer');
    drawer.classList.remove('drawer-open');
    drawer.classList.add('drawer-closed');
}

