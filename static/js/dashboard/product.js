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
