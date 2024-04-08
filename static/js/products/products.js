// function showProductDetails(name, description) {
//     // Create the popup element
//     var popup = document.createElement('div');
//     popup.classList.add('popup');

//     // Create the content for the popup
//     var content = document.createElement('div');
//     content.innerHTML = `
//         <img src="https://assets.sainsburys-groceries.co.uk/gol/8075006/1/640x640.jpg" alt="${name}" class="img-fluid mx-auto d-block">
//         <p class="productName">${name}</p>
//         <ul class="product-description">
//             ${description.map(desc => `<li>${desc}</li>`).join('')}
//         </ul>
//     `;

//     // Add content to popup
//     popup.appendChild(content);

//     // Add popup to the body
//     document.body.appendChild(popup);

//     // Close popup when clicked outside
//     popup.addEventListener('click', function(event) {
//         if (!content.contains(event.target)) {
//             popup.remove();
//         }
//     });
// }
