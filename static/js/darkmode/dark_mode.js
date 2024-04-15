const button = document.getElementById("darkModeButton");
const body = document.body;

function toggleDarkMode() {
    const isDarkMode = localStorage.getItem("darkMode") === "true";
    body.classList.toggle("dark-mode", !isDarkMode);
    localStorage.setItem("darkMode", !isDarkMode);
    button.querySelector("i").classList.toggle("fa-sun"); 
}

button.addEventListener("click", toggleDarkMode);

// Check on page load if dark mode was previously enabled
const storedDarkMode = localStorage.getItem("darkMode");
if (storedDarkMode !== null) {
    body.classList.toggle("dark-mode", storedDarkMode === "true");
    button.querySelector("i").classList.toggle("fa-sun", storedDarkMode === "true");  // Set initial icon
}