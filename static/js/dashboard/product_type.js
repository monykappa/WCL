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
