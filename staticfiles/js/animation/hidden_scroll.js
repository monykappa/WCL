function createObserver(selector) {
    return new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
            } else {
                entry.target.classList.remove('show');
            }
        });
    });
}

const observeElements = (observer, selector) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el) => observer.observe(el));
};

const observerLeft = createObserver('.hidden-left');
observeElements(observerLeft, '.hidden-left');

const observerRight = createObserver('.hidden-right');
observeElements(observerRight, '.hidden-right');

const observerTop = createObserver('.hidden-top');
observeElements(observerTop, '.hidden-top');

const observerBottom = createObserver('.hidden-bottom');
observeElements(observerBottom, '.hidden-bottom');
