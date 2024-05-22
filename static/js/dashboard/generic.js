// Define confirmDeleteGeneric function outside of DOMContentLoaded event listener
function confirmDeleteGeneric(genericId, genericName) {
    Swal.fire({
        title: 'Are you sure?',
        text: `Do you want to delete this generic '${genericName}'?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            // If confirmed, submit the form for deletion
            document.getElementById('deleteForm-' + genericId).submit();
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    // Function to filter the generic table based on input
    function filterGenericTable() {
        var input = document.getElementById('searchGenericInput').value.toLowerCase();
        var table = document.getElementById('genericTable');
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

    // Attach the filterGenericTable function to the input event of the search input
    document.getElementById('searchGenericInput').addEventListener('input', filterGenericTable);

    // Function to clear the search input and reset table filtering
    document.getElementById('clearGenericInput').addEventListener('click', function () {
        document.getElementById('searchGenericInput').value = '';
        filterGenericTable();
    });

    // Function to validate the form
    function validateForm() {
        var nameInput = document.getElementById('id_name').value.trim();
        if (nameInput === '') {
            Swal.fire({
                title: 'Error!',
                text: 'Please enter the generic name.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
            return false;
        }
        return true;
    }

    // Function to handle form submission
    function confirmFormSubmission(event) {
        event.preventDefault();
        if (validateForm()) {
            // Submit the form
            var form = document.getElementById('genericForm');
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
                            text: 'Generic added successfully!',
                            icon: 'success',
                            timer: 1000, // 1 second
                            timerProgressBar: true,
                            showConfirmButton: false
                        });

                        setTimeout(function () {
                            location.reload();
                        }, 1500); // Reload page after 1.5 seconds
                    } else {
                        // Show error message if form submission failed
                        Swal.fire({
                            title: 'Error!',
                            text: 'Failed to add generic. Please try again later.',
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
    document.getElementById('saveGenericBtn').addEventListener('click', confirmFormSubmission);

    // Attach the form submission function to the Enter key press event
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && $('#genericPopup').hasClass('show')) {
            confirmFormSubmission(event);
        }
    });

    // Your other functions and event listeners can go here...

});
