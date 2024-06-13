// Function to update the products page with current data
function updateProductPage() {
    let productTableBody = document.getElementById('productTableBody');
    productTableBody.innerHTML = ''; // Clear existing content

    // Retrieve products from localStorage
    let storedProducts = JSON.parse(localStorage.getItem('products')) || [];

    storedProducts.forEach(product => {
        let row = `
            <tr>
                <td>${product.name}</td>
                <td>${product.count}</td>
            </tr>
        `;
        productTableBody.innerHTML += row;
    });
}

// Initial update on page load
updateProductPage();
