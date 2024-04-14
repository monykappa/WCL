// Function to filter and update the table based on the search input
function filterTable() {
    var input = document.getElementById('searchInput').value.toLowerCase();
    var table = document.getElementById('drugTypeTable');
    var rows = table.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {
        var nameColumn = rows[i].getElementsByTagName('td')[0];
        var descriptionColumn = rows[i].getElementsByTagName('td')[1];
        if (nameColumn || descriptionColumn) {
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

document.getElementById('searchInput').addEventListener('input', filterTable);


document.getElementById('clearSearchInput').addEventListener('click', function() {
    document.getElementById('searchInput').value = ''; 
    filterTable(); 
});

    // Function to validate the form
    function validateForm() {
        try {
            var nameInput = document.getElementById('id_name').value.trim();
            if (nameInput === '') {
                Swal.fire("Error", "Please enter the product type name", "error");
            } else {
                submitForm();
            }
        } catch (error) {
            console.error("Error in validateForm:", error);
        }
    }

    // Function to handle form submission
    function submitForm() {
        var form = document.getElementById('productTypeForm');
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
                    text: 'Product type added successfully!',
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
                    text: 'Failed to add product type. Please try again later.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }