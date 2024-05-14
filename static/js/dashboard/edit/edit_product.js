

function openPackSizeWindow() {
    var packSizeButton = document.querySelector('.btn-primary[data-pack-size-url]');
    if (packSizeButton) {
        var packSizeUrl = packSizeButton.getAttribute('data-pack-size-url');
        openWindow(packSizeUrl);
    } else {
        console.error('Button with data-pack-size-url attribute not found.');
    }
}

function openCompositionWindow() {
    var compositionButton = document.querySelector('.btn-primary[data-composition-url]');
    if (compositionButton) {
        var compositionUrl = compositionButton.getAttribute('data-composition-url');
        openWindow(compositionUrl);
    } else {
        console.error('Button with data-composition-url attribute not found.');
    }
}




function openWindow(url) {
    var windowWidth = 400;
    var windowHeight = 400;
    var windowFeatures = "width=" + windowWidth + ",height=" + windowHeight + ",top=100,left=100";
    window.open(url, "_blank", windowFeatures);
}

// Function to show SweetAlert confirmation for form submission
function confirmFormSubmission(event) {
    event.preventDefault(); // Prevent the default form submission

    Swal.fire({
        title: 'Save Changes?',
        text: 'Are you sure you want to save the changes?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, save changes!'
    }).then((result) => {
        if (result.isConfirmed) {
            // Submit the form if confirmed
            document.getElementById('editProductForm').submit();
        }
    });
}

// Attach the confirmation function to the Enter key press event
document.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        confirmFormSubmission(event);
    }
});

// Attach the confirmation function to the button click event
document.getElementById('saveProductChangesButton').addEventListener('click', confirmFormSubmission);



function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function () {
        var imagePreview = document.createElement('img');
        imagePreview.src = reader.result;
        imagePreview.style.maxWidth = '100%';
        imagePreview.style.height = 'auto';
        var newImagePreviewContainer = document.getElementById('newImagePreviewContainer');
        newImagePreviewContainer.innerHTML = ''; // Clear previous image preview
        newImagePreviewContainer.appendChild(imagePreview);
    };
    reader.readAsDataURL(event.target.files[0]);
}