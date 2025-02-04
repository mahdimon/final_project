const REGISTER_API_URL = "/api/user/register/";

document.getElementById('registerForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const confirmPassword = document.getElementById('confirmPassword').value.trim();
    const errorMessage = document.getElementById('errorMessage');

    errorMessage.textContent = ""; // Clear previous errors

    // Client-side validation
    if (password !== confirmPassword) {
        errorMessage.textContent = "Passwords do not match.";
        return;
    }

    try {
        // Send registration data to the backend
        const response = await axios.post(REGISTER_API_URL, {
            username,
            email,
            password,
        });

        // Handle success: redirect to OTP page
        if (response.status === 200) {
            localStorage.setItem('email', email); // Store email for OTP validation
            window.location.href = "otp.html"; // Redirect to OTP page
        }
    } catch (error) {
        // Display backend validation errors
        if (error.response && error.response.data.error) {
            errorMessage.textContent = error.response.data.error;
        } else {
        
            errorMessage.textContent = "An unexpected error occurred.";
        }
    }
});
