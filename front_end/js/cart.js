const CART_API_URL = "/api/products/";
const CHECKOUT_URL = "/checkout/";
const LOGIN_URL = "/login/";

// Get cart from localStorage
function getCart() {
    return JSON.parse(localStorage.getItem("cart")) || {};
}

// Save cart to localStorage
function saveCart(cart) {
    localStorage.setItem("cart", JSON.stringify(cart));
}

// Fetch cart details from API
async function loadCart() {
    const cart = getCart();
    const productIds = Object.keys(cart);
    
    const cartContainer = document.getElementById("cartContainer");
    if (!cartContainer) {
        console.error("Cart container not found.");
        return;
    }

    if (productIds.length === 0) {
        cartContainer.innerHTML = "<p>Your cart is empty.</p>";
        return;
    }
    
    try {
        const response = await axios.get(CART_API_URL, { params: { id__in: productIds.join(",") } });
        const products = response.data;
        const updatedCart = {};
        cartContainer.innerHTML = "";

        products.forEach(product => {
            let quantity = cart[product.id];
            if (quantity > product.stock) {
                quantity = product.stock;
            }
            if (quantity > 0) {
                updatedCart[product.id] = quantity;
            }

            const itemDiv = document.createElement("div");
            itemDiv.classList.add("cart-item", "d-flex", "align-items-center", "mb-3", "p-2", "border", "rounded");
            itemDiv.innerHTML = `
                <img src="${product.image}" class="cart-item-image me-3" style="width: 80px; height: 80px; object-fit: cover; border-radius: 5px;">
                <div class="cart-item-details d-flex flex-column">
                    <p class="mb-1 fw-bold">${product.name}</p>
                    <p class="mb-1 text-muted">$${product.discounted_price || product.price}</p>
                    <div class="d-flex align-items-center">
                        <button class="btn btn-outline-danger btn-sm me-2" onclick="decreaseQuantity(${product.id}, ${product.stock})">-</button>
                        <span id="qty-${product.id}" class="mx-2">${quantity}</span>
                        <button class="btn btn-outline-success btn-sm ms-2" onclick="increaseQuantity(${product.id}, ${product.stock})">+</button>
                    </div>
                </div>
            `;
            cartContainer.appendChild(itemDiv);
        });

        saveCart(updatedCart);
    } catch (error) {
        console.error("Error loading cart items:", error);
    }
}

// Increase quantity
function increaseQuantity(productId, stock) {
    const cart = getCart();
    if (cart[productId] < stock) {
        cart[productId] += 1;
    } else {
        cart[productId] = 1
        
    }
    saveCart(cart);
    document.getElementById(`qty-${productId}`).innerText = cart[productId];
}

// Decrease quantity
function decreaseQuantity(productId) {
    const cart = getCart();
    if (cart[productId] > 2) {
        cart[productId] -= 1;
    } else {
        delete cart[productId]; // Remove from cart if quantity is 0
    }
    saveCart(cart);
    document.getElementById(`qty-${productId}`).innerText = cart[productId] || 0;
}

async function proceedToCheckout() {
    await loadNavbar(); 

    const accessToken = localStorage.getItem('accessToken');
    
    if (accessToken) {
        window.location.href = "checkout.html"; 
    } else {
        window.location.href = "login.html"; 
    }
}
// Load cart on page load
document.addEventListener("DOMContentLoaded", loadCart);
