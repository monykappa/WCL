document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById('id_image');
    const imagePreview = document.getElementById('imagePreview');

    imageInput.addEventListener('change', function (event) {
        const file = this.files[0];
        imagePreview.src = file ? URL.createObjectURL(file) : '#';
        imagePreview.style.display = file ? 'block' : 'none';
    });

    function validateForm() {
        var nameInput = document.getElementById('id_name').value.trim();
        if (nameInput === '') {
            Swal.fire({
                title: 'Error!',
                text: 'Please enter the product name.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
            return false;
        }
        return true;
    }

    function confirmFormSubmission(event) {
        event.preventDefault();
        if (validateForm()) {
            var form = document.getElementById('productForm');
            var formData = new FormData(form);

            fetch(form.action, {
                method: form.method,
                body: formData
            }).then(response => {
                if (response.ok) {
                    Swal.fire({
                        title: 'Success!',
                        text: 'Product added successfully!',
                        icon: 'success',
                        timer: 1000,
                        timerProgressBar: true,
                        showConfirmButton: false
                    });
                    setTimeout(function () { location.reload(); }, 1500);
                } else {
                    Swal.fire({
                        title: 'Error!',
                        text: 'Failed to add product. Please try again later.',
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                }
            }).catch(error => {
                console.error('Error:', error);
            });
        }
    }

    document.getElementById('saveProductBtn').addEventListener('click', confirmFormSubmission);

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && $('#productPopup').hasClass('show')) {
            confirmFormSubmission(event);
        }
    });

    function filterTable() {
        var input = document.getElementById('searchProductsInput').value.toLowerCase();
        var table = document.getElementById('productTable');
        var rows = table.getElementsByTagName('tr');

        for (var i = 0; i < rows.length; i++) {
            var cells = rows[i].getElementsByTagName('td');
            var isVisible = Array.from(cells).some(cell => cell.textContent.toLowerCase().includes(input));
            rows[i].style.display = isVisible ? '' : 'none';
        }
    }

    document.getElementById('searchProductsInput').addEventListener('input', filterTable);

    document.getElementById('clearProductInput').addEventListener('click', function () {
        document.getElementById('searchProductsInput').value = '';
        filterTable();
    });

    const deleteButtons = document.querySelectorAll('.delete-product');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const slug = this.dataset.slug;
            Swal.fire({
                title: 'Are you sure?',
                text: 'You will not be able to recover this product!',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'Cancel'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/dashboard/products/delete/${slug}/`, {
                        method: 'POST',
                        headers: { 'X-CSRFToken': '{{ csrf_token }}' }
                    }).then(response => response.json())
                        .then(data => {
                            Swal.fire('Deleted!', data.message, 'success');
                        }).catch(error => {
                            console.error('Error:', error);
                            Swal.fire('Error!', 'Failed to delete the product', 'error');
                        });
                }
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Handle click event on table rows
    document.querySelectorAll('.product-row').forEach(function(row) {
        row.addEventListener('click', function(event) {
            // Check if the click target is a button or a link within the row
            if (event.target.closest('button') || event.target.closest('a')) {
                return; // Do nothing if the click was on a button or a link
            }
            event.preventDefault();
            var productId = this.getAttribute('data-product');
            fetch('/dashboard/get_product_details/' + productId + '/')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                        return;
                    }

                    // Generate compositions display string
                    let compositionsDisplay = '';
                    data.compositions.forEach((comp, index) => {
                        if (index === 0) {
                            compositionsDisplay += `${comp.name}`;
                        } else {
                            compositionsDisplay += ` + ${comp.name}`;
                        }
                    });

                    // Populate modal with product data
                    var modalBody = document.getElementById('productModalBody');
                    modalBody.innerHTML = `
                        <div class="row">
                            <div class="col-md-4">
                                <p><strong>Name:</strong> ${data.name}</p>
                                <p><strong>Image:</strong></p><img src="${data.image}" alt="Product Image" class="img-fluid">
                            </div>
                            <div class="col-md-4">
                                <p><strong>Manufacturer:</strong> ${data.manufacturer}</p>
                                <p><strong>Category:</strong> ${data.category}</p>
                                <p><strong>Product Type:</strong> ${data.product_type}</p>
                                <p><strong>Generic:</strong> ${data.generic}</p>
                                <p><strong>Expiry Date:</strong> ${data.expiry_date}</p>
                                <p><strong>Created At:</strong> ${data.created_at}</p>
                                <p><strong>Updated At:</strong> ${data.updated_at}</p>
                            </div>
                            <div class="col-md-4">
                                <p><strong>Compositions:</strong> ${compositionsDisplay}</p>
                                <p><strong>Pack Sizes:</strong> ${data.pack_sizes.map(ps => ps.name).join(', ')}</p>
                                <p><strong>Description:</strong> ${data.description}</p>
                            </div>
                        </div>
                    `;
                    // Show modal
                    $('#productModal').modal('show');
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Handle error scenario (e.g., display error message to user)
                    alert('Product details could not be loaded. Please try again later.');
                });
        });
    });
});




function sortTableByPrice(order) {
    var table = document.getElementById('productTable').querySelector('tbody');
    var rows = Array.from(table.querySelectorAll('tr.product-row'));

    rows.sort(function(rowA, rowB) {
        var priceA = parseFloat(rowA.querySelector('td:nth-child(5)').innerText.replace('$', ''));
        var priceB = parseFloat(rowB.querySelector('td:nth-child(5)').innerText.replace('$', ''));

        if (order === 'desc') {
            return priceB - priceA; // Sort in descending order by price
        } else {
            return priceA - priceB; // Sort in ascending order by price
        }
    });

    // Re-append sorted rows to the table
    rows.forEach(function(row) {
        table.appendChild(row);
    });
}

function sortTableAlphabetically(order) {
    var table = document.getElementById('productTable').querySelector('tbody');
    var rows = Array.from(table.querySelectorAll('tr.product-row'));

    rows.sort(function(rowA, rowB) {
        var valueA = rowA.querySelector('td:nth-child(3)').innerText.trim(); // Assuming title is in the third column
        var valueB = rowB.querySelector('td:nth-child(3)').innerText.trim(); // Adjust this index based on your table structure

        if (order === 'desc') {
            return valueB.localeCompare(valueA); // Sort in descending order alphabetically
        } else {
            return valueA.localeCompare(valueB); // Sort in ascending order alphabetically
        }
    });

    // Re-append sorted rows to the table
    rows.forEach(function(row) {
        table.appendChild(row);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Sort the table initially by price in ascending order
    sortTableByPrice('asc');

    // Add event listener to the select dropdown for price sorting
    document.getElementById('sortPrice').addEventListener('change', function() {
        var sortOrder = this.value;
        sortTableByPrice(sortOrder);
    });

    // Add event listener to the select dropdown for alphabetical sorting
    document.getElementById('sortAlpha').addEventListener('change', function() {
        var sortOrder = this.value;
        sortTableAlphabetically(sortOrder);
    });
});

