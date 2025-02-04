const API_BASE_URL = "/api"; // Change to your backend URL

document.addEventListener("DOMContentLoaded", function () {
    checkAuth();
    loadUserProfile();
    loadUserAddresses();

    document.getElementById("userProfileForm").addEventListener("submit", updateUserProfile);
});

// Check authentication
function checkAuth() {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
        window.location.href = "login.html"; // Redirect to login if not authenticated
    }
}

// Fetch user profile data
async function loadUserProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/user/profile/`, {
            headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` }
        });

        if (response.status === 401) {
            await refreshToken();
            return loadUserProfile(); // Retry after refreshing token
        }

        if (!response.ok) throw new Error("Failed to fetch user data");

        const data = await response.json();
        document.getElementById("firstName").value = data.first_name;
        document.getElementById("lastName").value = data.last_name;
        document.getElementById("username").value = data.username;
        document.getElementById("email").value = data.email;
        document.getElementById("phone").value = data.phone_number;
    } catch (error) {
        console.error("Error loading user profile:", error);
    }
}

// Update user profile
async function updateUserProfile(event) {
    event.preventDefault();

    const updatedData = {
        first_name: document.getElementById("firstName").value,
        last_name: document.getElementById("lastName").value,
        phone_number: document.getElementById("phone").value,
    };

    try {
        const response = await fetch(`${API_BASE_URL}/user/profile/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            body: JSON.stringify(updatedData),
        });

        if (response.status === 401) {
            await refreshToken();
            return updateUserProfile(event); // Retry after refreshing token
        }

        if (!response.ok) throw new Error("Failed to update profile");

        alert("Profile updated successfully!");
    } catch (error) {
        console.error("Error updating profile:", error);
    }
}

// Fetch user addresses
async function loadUserAddresses() {
    try {
        const response = await fetch(`${API_BASE_URL}/user/addresses/`, {
            headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` }
        });

        if (!response.ok) throw new Error("Failed to fetch addresses");

        const addresses = await response.json();
        const container = document.getElementById("addressesContainer");
        container.innerHTML = "";

        addresses.forEach((address) => {
            const addressDiv = document.createElement("div");
            addressDiv.classList.add("card", "mb-3");
            addressDiv.setAttribute("data-address-id", address.id); // Unique identifier

            addressDiv.innerHTML = `
                <div class="card-body">
                    <p >City:<strong class="city">${address.city}</strong> </p>
                    <p >Province:<strong class="province">${address.province}</strong> </p>
                    <p >Address:<strong class="detailed-address">${address.detailed_address}</strong> </p>
                    <p >Postal Code:<strong class="postal-code">${address.postal_code}</strong> </p>
                    <button class="btn btn-warning btn-sm" onclick="editAddress(${address.id})">Edit</button>
                </div>
            `;

            container.appendChild(addressDiv);
        });
    } catch (error) {
        console.error("Error loading addresses:", error);
    }
}


// Refresh token if expired
async function refreshToken() {
    const refreshToken = localStorage.getItem("refreshToken");
    if (!refreshToken) {
        window.location.href = "login.html"; // Redirect to login
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/user/refresh/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (!response.ok) throw new Error("Failed to refresh token");

        const data = await response.json();
        localStorage.setItem("accessToken", data.access);
    } catch (error) {
        console.error("Error refreshing token:", error);
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        window.location.href = "login.html"; // Redirect to login
    }
}
document.addEventListener("DOMContentLoaded", function () {
    const addAddressBtn = document.getElementById("add-address-btn");
    const newAddressForm = document.getElementById("new-address-form");
    const saveAddressBtn = document.getElementById("save-address-btn");
    const cancelAddressBtn = document.getElementById("cancel-address-btn");

    // Show the address form when clicking "Add New Address"
    addAddressBtn.addEventListener("click", function () {
        newAddressForm.style.display = "block";
    });

    // Hide the form when clicking "Cancel"
    cancelAddressBtn.addEventListener("click", function () {
        newAddressForm.style.display = "none";
    });

    // Handle saving a new address
    saveAddressBtn.addEventListener("click", function () {
        const city = document.getElementById("new-city").value;
        const province = document.getElementById("new-province").value;
        const detailedAddress = document.getElementById("new-detailed-address").value;
        const postalCode = document.getElementById("new-postal-code").value;

        const accessToken = localStorage.getItem("accessToken");

        if (!accessToken) {
            alert("You need to be logged in to add an address.");
            return;
        }

        fetch(`${API_BASE_URL}/user/addresses/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                city: city,
                province: province,
                detailed_address: detailedAddress,
                postal_code: postalCode
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                alert("Address added successfully!");
                location.reload(); // Refresh the page to show the new address
            } else {
                alert("Failed to add address. Please check your inputs.");
            }
        })
        .catch(error => console.error("Error:", error));
    });
});

function editAddress(addressId) {
    const addressDiv = document.querySelector(`[data-address-id="${addressId}"]`);

    if (!addressDiv) return;

    // Extract current values
    const city = addressDiv.querySelector(".city").textContent;
    const province = addressDiv.querySelector(".province").textContent;
    const detailedAddress = addressDiv.querySelector(".detailed-address").textContent;
    const postalCode = addressDiv.querySelector(".postal-code").textContent;

    // Replace content with input fields
    addressDiv.innerHTML = `
        <div class="card-body">
            <label><strong>City:</strong></label>
            <input type="text" class="form-control mb-2" id="edit-city-${addressId}" value="${city}">

            <label><strong>Province:</strong></label>
            <input type="text" class="form-control mb-2" id="edit-province-${addressId}" value="${province}">

            <label><strong>Address:</strong></label>
            <textarea class="form-control mb-2" id="edit-detailed-address-${addressId}">${detailedAddress}</textarea>

            <label><strong>Postal Code:</strong></label>
            <input type="text" class="form-control mb-2" id="edit-postal-code-${addressId}" value="${postalCode}">

            <button class="btn btn-success btn-sm" onclick="saveAddress(${addressId})">Save</button>
            <button class="btn btn-secondary btn-sm" onclick="cancelEdit(${addressId}, '${city}', '${province}', '${detailedAddress}', '${postalCode}')">Cancel</button>
        </div>
    `;
}

// Save the updated address
async function saveAddress(addressId) {
    const updatedData = {
        city: document.getElementById(`edit-city-${addressId}`).value,
        province: document.getElementById(`edit-province-${addressId}`).value,
        detailed_address: document.getElementById(`edit-detailed-address-${addressId}`).value,
        postal_code: document.getElementById(`edit-postal-code-${addressId}`).value,
    };

    try {
        const response = await fetch(`${API_BASE_URL}/user/addresses/${addressId}/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            body: JSON.stringify(updatedData),
        });

        if (!response.ok) throw new Error("Failed to update address");

        alert("Address updated successfully!");
        location.reload(); // Refresh the page to show updated address
    } catch (error) {
        console.error("Error updating address:", error);
    }
}

// Cancel editing and restore original data
function cancelEdit(addressId, city, province, detailedAddress, postalCode) {
    const addressDiv = document.querySelector(`[data-address-id="${addressId}"]`);
    addressDiv.innerHTML = `
        <div class="card-body">
            <p class="city"><strong>City:</strong> ${city}</p>
            <p class="province"><strong>Province:</strong> ${province}</p>
            <p class="detailed-address"><strong>Address:</strong> ${detailedAddress}</p>
            <p class="postal-code"><strong>Postal Code:</strong> ${postalCode}</p>
            <button class="btn btn-warning btn-sm" onclick="editAddress(${addressId})">Edit</button>
        </div>
    `;
}
