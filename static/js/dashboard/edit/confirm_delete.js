// Alert delete for category
function confirmDelete(categoryId) {
    Swal.fire({
        title: 'Are you sure?',
        text: 'You are about to delete this category. This action cannot be undone!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            // If confirmed, submit the form to delete the category
            document.getElementById('deleteForm-' + categoryId).submit();
        }
    });
}


// Alert delete for manufacturer
function confirmDeleteManufacturer(manufacturerId) {
    Swal.fire({
        title: 'Are you sure?',
        text: 'You are about to delete this manufacturer. This action cannot be undone!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            // If confirmed, submit the form to delete the manufacturer
            document.getElementById('deleteForm-' + manufacturerId).submit();
        }
    });
}