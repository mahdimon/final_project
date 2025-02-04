async function loadNavbar() {
    // Fetch and inject the navbar
    const response = await fetch('navbar.html');
    const navbarHTML = await response.text();
    const existingNavbar = document.getElementById('navbar');
    if (existingNavbar) {
      existingNavbar.remove();
    }
    document.body.insertAdjacentHTML('afterbegin', navbarHTML);
    const navbarLinks = document.getElementById('navbarLinks');

    // Check authentication state
    let accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');

    let username = null;
    let isAuthenticated = false;

    if (accessToken) {
        isAuthenticated = await verifyToken(accessToken);
    }

    if (!isAuthenticated && refreshToken) {
        const newAccessToken = await refreshAccessToken(refreshToken);
        if (newAccessToken) {
            isAuthenticated = await verifyToken(newAccessToken);
            accessToken = newAccessToken;
        }

    }

    // Update navbar based on authentication state
    if (isAuthenticated) {
        username = await getUsername(accessToken || localStorage.getItem('accessToken'));
        navbarLinks.innerHTML = `
            <li class="nav-item">
                <span class="nav-link">Hi, ${username}</span>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="dashboard.html">User dashboard</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="order-history.html">order history</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#" id="logoutButton">Logout</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="cart.html">Cart</a>
            </li>
        `;

        // Logout functionality
        document.getElementById('logoutButton').addEventListener('click', () => {
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            location.reload();
        });
    } else {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        
        navbarLinks.innerHTML = `
            <li class="nav-item">
                <a class="nav-link" href="register.html">Register</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="login.html">Login</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="cart.html">Cart</a>
            </li>
        `;
    }
}

async function verifyToken(token) {
    try {
        const response = await fetch('/api/user/verify/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token }),
        });

        return response.status === 200;
    } catch (error) {
        console.error('Token verification failed:', error);
        return false;
    }
}

async function refreshAccessToken(refreshToken) {
    try {
        const response = await fetch('/api/user/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (response.status === 200) {
            const data = await response.json();
            localStorage.setItem('accessToken', data.access);
            return data.access;
        }
    } catch (error) {
        console.error('Token refresh failed:', error);
    }
    return null;
}

async function getUsername(accessToken) {
    try {
        const response = await fetch('/api/user/user-info/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            },
        });

        if (response.status === 200) {
            const data = await response.json();
            return data.username;
        }
    } catch (error) {
        console.error('Failed to fetch user info:', error);
    }
    return 'User';
}

// Load navbar on page load
loadNavbar()
// document.addEventListener('DOMContentLoaded', loadNavbar);
