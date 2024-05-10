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

document.addEventListener('DOMContentLoaded', function () {
    const galleryImages = document.querySelectorAll('.gallery-img');

    galleryImages.forEach(function (img) {
        img.addEventListener('click', function () {
            showFullScreen(this);
        });
    });

    function showFullScreen(element) {
        const fullscreenDiv = document.getElementById('fullscreen');
        const fullscreenImg = document.getElementById('fullscreen-img');
        const body = document.body;

        fullscreenImg.src = element.src;

        fullscreenDiv.style.display = 'flex';
        body.style.overflow = 'hidden';

        fullscreenImg.style.transform = 'scale(1)';
    }
});
