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
