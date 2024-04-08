document.addEventListener("DOMContentLoaded", function () {
    // Delay before applying fly-in animation
    setTimeout(() => {
        const titleElement = document.querySelector('.slide.active .slide-title h1');
        titleElement.style.animation = 'flyIn 1s forwards'; // Apply fly-in animation
    }, 1000); // 1 second delay before applying the animation

    // Start the slide change interval after a delay
    setTimeout(startSlideChange, 1000);
});

let slideIndex = 0;
const slides = document.querySelector('.slides');
const totalSlides = document.querySelectorAll('.slide').length;
let slideChangeTimeout; // Variable to hold the slide change timeout

function moveSlide(n) {
    // Clear the automatic slide change timeout
    clearTimeout(slideChangeTimeout);

    slideIndex += n;

    // Ensure slideIndex stays within the range of slides
    if (slideIndex >= totalSlides) {
        slideIndex = 0;
    } else if (slideIndex < 0) {
        slideIndex = totalSlides - 1;
    }

    // Hide all slides
    document.querySelectorAll('.slide').forEach(slide => {
        slide.classList.remove('active');
    });

    // Show current slide
    const currentSlide = document.querySelectorAll('.slide')[slideIndex];
    currentSlide.classList.add('active');

    // Apply fly-in animation to the title
    const titleElement = currentSlide.querySelector('.slide-title h1');
    titleElement.style.animation = 'flyIn 1s forwards'; // Apply fly-in animation

    // Start the slide change interval
    startSlideChange();
}

function startSlideChange() {
    // Automatic slide change every 7 seconds
    slideChangeTimeout = setTimeout(() => {
        moveSlide(1);
    }, 7000);
}
