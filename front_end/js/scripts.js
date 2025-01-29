const CATEGORY_API_URL = "http://127.0.0.1:8000/api/products/categories/";
const PRODUCT_API_URL = "http://127.0.0.1:8000/api/products/";

let selectedCategoryId = null; // Track selected category
let categories = []; // Store all categories for filtering

// Helper: Get cart from localStorage
function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || {};
}

// Helper: Save cart to localStorage
function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
}


        // Add product to cart
        function addToCart(productId, stock, button) {
            const cart = getCart();
            cart[productId] = 1; // Add 1 item to the cart
            saveCart(cart);

            // Update the UI to show the counter
            const container = button.parentElement;
            updateCartUI(productId, stock, container);
        }

        // Increase product quantity in the cart
        function increaseQuantity(productId, stock, button) {
            const cart = getCart();
            const currentQty = cart[productId] || 0;

            if (currentQty < stock) {
                cart[productId] = currentQty + 1;
                saveCart(cart);

                // Update the UI
                const container = button.parentElement.parentElement;
                updateCartUI(productId, stock, container);
            }
        }

        // Decrease product quantity in the cart
        function decreaseQuantity(productId, stock, button) {
            const cart = getCart();
            const currentQty = cart[productId] || 0;

            if (currentQty > 1) {
                cart[productId] = currentQty - 1;
                saveCart(cart);

                // Update the UI
                const container = button.parentElement.parentElement;
                updateCartUI(productId, stock, container);
            } else {
                // Remove the product from the cart if the quantity is 0
                delete cart[productId];
                saveCart(cart);

                // Revert to "Add to Cart" button
                const container = button.parentElement.parentElement;
                updateCartUI(productId, stock, container);
            }
        }


// Update Cart UI
function updateCartUI(productId, stock, container) {
    const cart = getCart();
    const currentQty = cart[productId] || 0;

    if (currentQty > 0) {
        container.innerHTML = `
            <div class="d-flex align-items-center">
                <button class="btn btn-outline-danger btn-sm" onclick="decreaseQuantity(${productId}, ${stock}, this)">-</button>
                <span class="mx-2">${currentQty}</span>
                <button class="btn btn-outline-success btn-sm" onclick="increaseQuantity(${productId}, ${stock}, this)">+</button>
            </div>
        `;
    } else {
        container.innerHTML = `
            <button class="btn btn-primary" onclick="addToCart(${productId}, ${stock}, this)">Add to Cart</button>
        `;
    }
}
// Example: Collect category IDs recursively
function collectCategoryIds(category) {
    const ids = [category.id];
    if (category.subcategories && category.subcategories.length > 0) {
        category.subcategories.forEach(subcategory => {
            ids.push(...collectCategoryIds(subcategory)); // Add subcategory IDs
        });
    }
    return ids;
}

// Helper function: Flatten category tree into a list
function flattenCategories(categories) {
    const flatList = [];

    function traverse(categoryList) {
        categoryList.forEach(category => {
            flatList.push(category); // Add current category
            if (category.subcategories && category.subcategories.length > 0) {
                traverse(category.subcategories); // Recursively add subcategories
            }
        });
    }

    traverse(categories);
    return flatList;
}

// Main function to get filters
function getFilters() {
    const name = document.getElementById('searchName').value.trim();
    const minPrice = document.getElementById('minPrice').value.trim();
    const maxPrice = document.getElementById('maxPrice').value.trim();

    const filters = {};
    if (selectedCategoryId) {
        // Flatten the category tree and find the selected category
        const allCategories = flattenCategories(categories); // Flattened list of all categories
        const selectedCategory = allCategories.find(cat => cat.id == selectedCategoryId);

        if (selectedCategory) {
            // Collect IDs of the selected category and its subcategories
            const categoryIds = collectCategoryIds(selectedCategory);
            filters['category__id__in'] = categoryIds.join(','); // Pass as comma-separated string
        }
    }

    if (name) filters['search'] = name; // Filter by name
    if (minPrice) filters['price__gte'] = minPrice; // Minimum price
    if (maxPrice) filters['price__lte'] = maxPrice; // Maximum price

    return filters;
}

// Load products from the API
async function loadProducts(extraFilters = {}) {
    try {
        const filters = getFilters();
        const response = await axios.get(PRODUCT_API_URL, { params: { ...filters, ...extraFilters } });
        const products = response.data.results || response.data;

        const productList = document.getElementById('productList');
        productList.innerHTML = "";

        products.forEach(product => {
            let priceHTML = `<p class="fw-bold">Price: $${product.price}</p>`;
            if (product.discounted_price && product.discounted_price != product.price) {
                priceHTML = `
                    <p class="text-muted text-decoration-line-through">Price: $${product.price}</p>
                    <p class="fw-bold text-danger">Discounted Price: $${product.discounted_price}</p>
                `;
            }

            const productCard = `
                <div class="col">
                    <div class="card h-100">
                        <img src="${product.image}" class="card-img-top" alt="${product.name}">
                        <div class="card-body">
                            <h5 class="card-title">
                                <a href="product_detail.html?id=${product.id}" class="text-decoration-none">${product.name}</a>
                            </h5>
                            ${priceHTML}
                            <div id="cartButtonContainer-${product.id}">
                                <!-- Cart buttons will be dynamically updated -->
                            </div>
                        </div>
                    </div>
                </div>
            `;
            productList.innerHTML += productCard;

            // Update the cart UI for each product
            const cartButtonContainer = document.getElementById(`cartButtonContainer-${product.id}`);
            updateCartUI(product.id, product.stock, cartButtonContainer);
        });
    } catch (error) {
        console.error("Error fetching products:", error);
    }
}

// Load categories from the API
async function loadCategories() {
    try {
        const response = await axios.get(CATEGORY_API_URL);
        categories = response.data;

        const categoryList = document.getElementById('categoryList');
        categoryList.innerHTML = "";

        function renderCategories(categories, parentElement) {
            categories.forEach(category => {
                const listItem = document.createElement('li');
                listItem.className = 'list-group-item';
                listItem.textContent = category.name;

                listItem.addEventListener('click', () => {
                    selectedCategoryId = category.id;
                    
                    loadProducts();
                });

                parentElement.appendChild(listItem);

                // Render subcategories recursively
                if (category.subcategories && category.subcategories.length > 0) {
                    const subCategoryList = document.createElement('ul');
                    subCategoryList.className = 'list-group ms-4 mt-2';
                    renderCategories(category.subcategories, subCategoryList);
                    parentElement.appendChild(subCategoryList);
                }
            });
        }

        renderCategories(categories, categoryList);
    } catch (error) {
        console.error("Error fetching categories:", error);
    }
}
async function loadProductDetail() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');

    if (!productId) {
        console.error("Product ID not provided in the URL.");
        return;
    }

    try {
        const response = await axios.get(`${PRODUCT_API_URL}${productId}/`);
        const product = response.data;

        const productDetail = document.getElementById('productDetail');

        let priceHTML = `<p class="fw-bold">Price: $${product.price}</p>`;
        if (product.discounted_price && product.discounted_price != product.price) {
            priceHTML = `
                <p class="text-muted text-decoration-line-through">Price: $${product.price}</p>
                <p class="fw-bold text-danger">Discounted Price: $${product.discounted_price}</p>
            `;
        }

        productDetail.innerHTML = `
            <div class="col-md-6">
                <img src="${product.image}" class="img-fluid" alt="${product.name}">
            </div>
            <div class="col-md-6">
                <h2>${product.name}</h2>
                ${priceHTML}
                <p>${product.description || "No description available."}</p>
                <div id="cartButtonContainer-${product.id}">
                    <button class="btn btn-primary" onclick="addToCart(${product.id}, ${product.stock}, this)">Add to Cart</button>
                </div>
            </div>
        `;

        // Initialize the cart button UI
        const cartButtonContainer = document.getElementById(`cartButtonContainer-${product.id}`);
        updateCartUI(product.id, product.stock, cartButtonContainer);
    } catch (error) {
        console.error("Error fetching product detail:", error);
    }
}

