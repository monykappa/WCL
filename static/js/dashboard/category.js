document.addEventListener("DOMContentLoaded", function() {
    // Function to filter and update the table based on the search input
    function filterTable() {
        var input = document.getElementById('searchInput').value.toLowerCase();
        var table = document.getElementById('categoryTable');
        var rows = table.getElementsByTagName('tr');
        for (var i = 0; i < rows.length; i++) {
            var nameColumn = rows[i].getElementsByTagName('td')[0];
            var descriptionColumn = rows[i].getElementsByTagName('td')[1];
            if (nameColumn && descriptionColumn) {
                var nameText = nameColumn.textContent || nameColumn.innerText;
                var descriptionText = descriptionColumn.textContent || descriptionColumn.innerText;
                if (nameText.toLowerCase().indexOf(input) > -1 || descriptionText.toLowerCase().indexOf(input) > -1) {
                    rows[i].style.display = '';
                } else {
                    rows[i].style.display = 'none';
                }
            }
        }
    }

    // Add event listener for input changes in search input
    document.getElementById('searchInput').addEventListener('input', filterTable);

    // Add event listener for clearing the search input
    document.getElementById('clearSearchInput').addEventListener('click', function() {
        document.getElementById('searchInput').value = ''; 
        filterTable(); 
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Function to validate the form
    function validateForm() {
        var categoryName = document.getElementById('category_name').value.trim();
        if (categoryName === '') {
            Swal.fire({
                title: 'Error!',
                text: 'Please enter a category name.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
            return false;
        }
        return true;
    }

    // Function to handle form submission without confirmation
    function confirmFormSubmission(event) {
        event.preventDefault();
        if (validateForm()) {
            // Submit the form
            var form = document.getElementById('categoryForm');
            var formData = new FormData(form);

            fetch(form.action, {
                method: form.method,
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    // Show success message
                    Swal.fire({
                        title: 'Success!',
                        text: 'Category added successfully!',
                        icon: 'success',
                        timer: 1000, // 2 seconds
                        timerProgressBar: true,
                        showConfirmButton: false
                    });
                    
                    setTimeout(function() {
                        location.reload();
                    }, 1500);
                } else {
                    // Show error message if form submission failed
                    Swal.fire({
                        title: 'Error!',
                        text: 'Failed to add category. Please try again later.',
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }

    // Attach the form submission function to the "Save" button click event
    document.getElementById('saveCategoryBtn').addEventListener('click', confirmFormSubmission);

    // Attach the form submission function to the Enter key press event
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && $('#categoryPopup').hasClass('show')) {
            confirmFormSubmission(event);
        }
    });
});

