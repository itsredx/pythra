// web/main.js

function handleClick(callback_name) {
    if (window.pywebview) {
        window.pywebview.on_pressed_str(callback_name).then(function(response) {
            console.log(response);
        }).catch(function(error) {
            console.error(error);
        });
    } else {
        console.error('pywebview is not defined');
    }
}

function handleClickOnTap(callback_name, ...args) {
    if (window.pywebview) {
        console.log("index", args);
        window.pywebview.on_pressed(callback_name, ...args).then(function(response) {
            console.log(response);
        }).catch(function(error) {
            console.error(error);
        });
    } else {
        console.error('pywebview is not defined');
    }
}

new QWebChannel(qt.webChannelTransport, function(channel) {
    window.pywebview = channel.objects.pywebview;
});

const leftDrawer = document.getElementById('leftDrawer');
const rightDrawer = document.getElementById('rightDrawer');
const content = document.getElementById('content');
const bottomNav = document.getElementById('bottomNav');
const appBar = document.querySelector('.app-bar');

function toggleDrawer(side) {
    const drawer = side === 'left' ? leftDrawer : rightDrawer;
    const isOpen = drawer.classList.contains('open');

    if (isOpen) {
        drawer.classList.remove('open');
        updateLayout();
    } else {
        drawer.classList.add('open');
        bottomNav.classList.add('hidden');
        updateLayout();
    }

    if (!leftDrawer.classList.contains('open') && !rightDrawer.classList.contains('open')) {
        bottomNav.classList.remove('hidden');
    }
}

function updateLayout() {
    const leftOpen = leftDrawer.classList.contains('open');
    const rightOpen = rightDrawer.classList.contains('open');

    content.style.marginLeft = leftOpen ? '250px' : '0';
    content.style.marginRight = rightOpen ? '250px' : '0';
    appBar.style.marginLeft = leftOpen ? '250px' : '0';
    appBar.style.marginRight = rightOpen ? '250px' : '0';
}




/*
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

*/