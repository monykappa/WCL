const observerLeft = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
        }
        else {
            entry.target.classList.remove('show')
        }

    });
});

const hiddenElementLeft = document.querySelectorAll('.hidden-left');
hiddenElementLeft.forEach((el) => observerLeft.observe(el));


const observerRight = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
        }
        else {
            entry.target.classList.remove('show')
        }

    });
});

const hiddenElementRight = document.querySelectorAll('.hidden-right');
hiddenElementRight.forEach((el) => observerRight.observe(el));