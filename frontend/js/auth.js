// Authentication JavaScript

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.classList.add('show');
}

function hideError() {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = '';
    errorDiv.classList.remove('show');
}

// Login form handler
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        
        try {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Logging in...';
            
            const response = await apiClient.login(username, password);
            
            // Store token
            apiClient.setToken(response.token);
            
            // Redirect to main app
            window.location.href = 'app.html';
            
        } catch (error) {
            showError(error.message);
            submitBtn.disabled = false;
            submitBtn.textContent = 'Log In';
        }
    });
}

// Register form handler
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const submitBtn = registerForm.querySelector('button[type="submit"]');
        
        try {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Creating account...';
            
            const response = await apiClient.register(username, email, password);
            
            // Store token
            apiClient.setToken(response.token);
            
            // Redirect to main app
            window.location.href = 'app.html';
            
        } catch (error) {
            showError(error.message);
            submitBtn.disabled = false;
            submitBtn.textContent = 'Sign Up';
        }
    });
}
