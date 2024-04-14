function filterManufacturerTable() {
    var input = document.getElementById('searchManufacturerInput').value.toLowerCase();
    var table = document.getElementById('manufacturerTable');
    var rows = table.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {
        var nameColumn = rows[i].getElementsByTagName('td')[0];
        var countryColumn = rows[i].getElementsByTagName('td')[1];
        var descriptionColumn = rows[i].getElementsByTagName('td')[2];
        if (nameColumn || countryColumn || descriptionColumn) {
            var nameText = nameColumn.textContent || nameColumn.innerText;
            var countryText = countryColumn.textContent || countryColumn.innerText;
            var descriptionText = descriptionColumn.textContent || descriptionColumn.innerText;
            if (nameText.toLowerCase().indexOf(input) > -1 || countryText.toLowerCase().indexOf(input) > -1 || descriptionText.toLowerCase().indexOf(input) > -1) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    }
}

document.getElementById('searchManufacturerInput').addEventListener('input', filterManufacturerTable);

document.getElementById('clearManufacturerInput').addEventListener('click', function () {
    document.getElementById('searchManufacturerInput').value = '';
    filterManufacturerTable();
});

document.addEventListener("DOMContentLoaded", function () {
    // Function to validate the form
    function validateForm() {
        var nameInput = document.getElementById('id_name').value.trim();
        if (nameInput === '') {
            Swal.fire({
                title: 'Error!',
                text: 'Please enter the manufacturer name.',
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
            var form = document.getElementById('manufacturerForm');
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
                        text: 'Manufacturer added successfully!',
                        icon: 'success',
                        timer: 1000, // 1 second
                        timerProgressBar: true,
                        showConfirmButton: false
                    });
                    
                    setTimeout(function() {
                        location.reload();
                    }, 1500); // Reload page after 1.5 seconds
                } else {
                    // Show error message if form submission failed
                    Swal.fire({
                        title: 'Error!',
                        text: 'Failed to add manufacturer. Please try again later.',
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
    document.getElementById('saveManufacturerBtn').addEventListener('click', confirmFormSubmission);

    // Attach the form submission function to the Enter key press event
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && $('#manufacturerPopup').hasClass('show')) {
            confirmFormSubmission(event);
        }
    });
});


