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
