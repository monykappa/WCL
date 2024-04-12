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
