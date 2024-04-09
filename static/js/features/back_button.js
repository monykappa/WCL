document.addEventListener("DOMContentLoaded", function() {

    const backButton = document.getElementById("backButton");

    backButton.addEventListener("click", function(event) {
        event.preventDefault();

        window.history.back();
    });
});