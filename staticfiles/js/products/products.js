function showModal(productElement) {
    var modal = document.getElementById("productModal");
    var modalContent = modal.querySelector(".modal-content");
    var productName = productElement.querySelector(".productName").innerText;
    var productDescription = productElement.querySelector(".product-description").innerHTML;
    var imageURL = productElement.querySelector("img").src;

    // Set content
    var modalProductName = modalContent.querySelector("#productName");
    var modalDescription = modalContent.querySelector("#description");
    var modalImage = modalContent.querySelector("#modal-image");

    modalProductName.innerText = productName;
    modalDescription.innerHTML = productDescription;
    modalImage.src = imageURL;

    // Show modal with animation
    modal.style.display = "block";
    setTimeout(function () {
        modalContent.style.opacity = "1";
        modalContent.style.transform = "translate(-50%, -50%)";
        document.body.classList.add("modal-open");
        productElement.querySelector(".product-description").classList.remove("hidden");
    }, 50);
}

function closeModal() {
    var modal = document.getElementById("productModal");
    var modalContent = modal.querySelector(".modal-content");

    // Hide modal with animation
    modalContent.style.opacity = "0";
    modalContent.style.transform = "translate(-50%, -200%)";
    document.body.classList.remove("modal-open");
    setTimeout(function () {
        modal.style.display = "none";
    }, 300);
}




function showFullScreen(element) {
    const fullscreenDiv = document.getElementById('fullscreen');
    const fullscreenImg = document.getElementById('fullscreen-img');
    const body = document.body;
    
    const img = element.querySelector('img');
    fullscreenImg.src = img.src;

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
