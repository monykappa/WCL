document.addEventListener("DOMContentLoaded", function() {
    // Function to filter and update the table based on the search input
    function filterTable() {
        var input = document.getElementById('searchInput').value.toLowerCase();
        var table = document.querySelector('.table');
        var rows = table.getElementsByTagName('tr');
        for (var i = 0; i < rows.length; i++) {
            var titleColumn = rows[i].getElementsByTagName('td')[0];
            var descriptionColumn = rows[i].getElementsByTagName('td')[1];
            if (titleColumn && descriptionColumn) {
                var titleText = titleColumn.textContent || titleColumn.innerText;
                var descriptionText = descriptionColumn.textContent || descriptionColumn.innerText;
                if (titleText.toLowerCase().indexOf(input) > -1 || descriptionText.toLowerCase().indexOf(input) > -1) {
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

function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var imagePreview = document.getElementById('imagePreview');
        imagePreview.src = reader.result;
        imagePreview.style.display = 'block';
    }
    reader.readAsDataURL(event.target.files[0]);
}

function validateForm() {
    try {
        var titleInput = document.getElementById('title');
        if (titleInput && titleInput.value.trim() === '') {
            Swal.fire("Error", "Please enter the title", "error");
        } else {
            // Show SweetAlert immediately upon form submission
            Swal.fire({
                title: "Success",
                text: "News added",
                icon: "success",
                timer: 1000, // Set timer to 1000 milliseconds (1 second)
                showConfirmButton: false // Hide the "Okay" button
            });

            // Submit the form after a slight delay to allow SweetAlert to appear
            setTimeout(function() {
                document.getElementById('myForm').submit();
            }, 1000); // Adjust the delay time as needed (in milliseconds)
        }
    } catch (error) {
        console.error("Error in validateForm:", error);
    }
}

