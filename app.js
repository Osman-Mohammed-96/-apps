// Add your JavaScript code here

document.addEventListener('DOMContentLoaded', function() {
    loadProducts();

    // Handle form submission
    document.getElementById('add-product-form').addEventListener('submit', function(event) {
        event.preventDefault();
        addProduct();
    });
});

function loadProducts() {
    fetch('/get_products')
        .then(response => response.json())
        .then(products => {
            const productList = document.getElementById('product-list');
            productList.innerHTML = '';

            products.forEach(product => {
                const productDiv = document.createElement('div');
                productDiv.classList.add('product');

                const productName = document.createElement('p');
                productName.classList.add('product-name');
                productName.textContent = product.name;

                const productPrice = document.createElement('p');
                productPrice.classList.add('product-price');
                productPrice.textContent = `$${product.price.toFixed(2)}`;

                productDiv.appendChild(productName);
                productDiv.appendChild(productPrice);
                productList.appendChild(productDiv);
            });
        });
}

function addProduct() {
    const productName = document.getElementById('productName').value;
    const productPrice = document.getElementById('productPrice').value;

    fetch('/add_product', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `productName=${productName}&productPrice=${productPrice}`,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        loadProducts(); // Reload products after adding a new one
    });
}
