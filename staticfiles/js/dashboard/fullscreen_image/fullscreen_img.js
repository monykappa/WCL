// Add event listener to all elements with the class 'image-fullscreen-trigger'
document.querySelectorAll('.image-fullscreen-trigger').forEach(item => {
    item.addEventListener('click', event => {
        showFullScreen(item); // Call showFullScreen function when clicked
    });
});

function showFullScreen(element) {
    const fullscreenDiv = document.getElementById('fullscreen');
    const fullscreenImg = document.getElementById('fullscreen-img');
    const body = document.body;

    fullscreenImg.src = element.src; // Set the source of the full screen image to the clicked image source

    fullscreenDiv.style.display = 'flex';
    body.style.overflow = 'hidden';

    fullscreenImg.style.transform = 'scale(1)';
}

function closeFullScreen() {
    const fullscreenDiv = document.getElementById('fullscreen');
    const body = document.body;

    fullscreenDiv.style.display = 'none';
    body.style.overflow = 'auto';
}

function zoomIn() {
    const fullscreenImg = document.getElementById('fullscreen-img');
    const currentScale = parseFloat(fullscreenImg.style.transform.match(/(\d+(?:\.\d+)?)/)[0]);
    const newScale = currentScale + 0.2;

    fullscreenImg.style.transform = `scale(${newScale})`;
}

function zoomOut() {
    const fullscreenImg = document.getElementById('fullscreen-img');
    const currentScale = parseFloat(fullscreenImg.style.transform.match(/(\d+(?:\.\d+)?)/)[0]);
    const newScale = Math.max(currentScale - 0.2, 1);

    fullscreenImg.style.transform = `scale(${newScale})`;
}