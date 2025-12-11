// API Configuration
const API_BASE_URL = 'http://localhost:5001/api';

// DOM Elements
let loginForm, registerForm, logoutBtn, loginLink, registerLink, userMenu, usernameDisplay;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check authentication status on page load
    checkAuthStatus();
    
    // Initialize login form
    if (document.getElementById('login-form')) {
        loginForm = document.getElementById('login-form');
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Initialize register form
    if (document.getElementById('register-form')) {
        registerForm = document.getElementById('register-form');
        registerForm.addEventListener('submit', handleRegister);
    }
    
    // Initialize logout button
    logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
    
    // Load posts if on homepage
    if (window.location.pathname === '/' || window.location.pathname.includes('index.html')) {
        if (typeof loadPosts === 'function') {
            loadPosts();
        }
    }
});

// Check if user is authenticated
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    
    // Get DOM elements
    userMenu = document.getElementById('user-menu');
    loginLink = document.getElementById('login-link');
    registerLink = document.getElementById('register-link');
    usernameDisplay = document.getElementById('username-display');
    dashboardLink = document.getElementById('dashboard-link');
    
    if (token && username && userMenu && loginLink && registerLink) {
        // User is logged in
        userMenu.style.display = 'flex';
        loginLink.style.display = 'none';
        registerLink.style.display = 'none';
        if (usernameDisplay) usernameDisplay.textContent = 'Hi, ' + username;
        if (dashboardLink) dashboardLink.style.display = 'block';
    } else if (userMenu && loginLink && registerLink) {
        // User is not logged in
        userMenu.style.display = 'none';
        loginLink.style.display = 'block';
        registerLink.style.display = 'block';
        if (dashboardLink) dashboardLink.style.display = 'none';
    }
}

// Handle Login
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const messageDiv = document.getElementById('login-message');
    
    // Validate inputs
    if (!username || !password) {
        showMessage(messageDiv, 'Please fill in all fields', 'error');
        return;
    }
    
    try {
        const response = await fetch(API_BASE_URL + '/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Save token and user info
            localStorage.setItem('token', data.token);
            localStorage.setItem('username', data.user.username);
            localStorage.setItem('user_id', data.user.id);
            
            showMessage(messageDiv, 'Login successful! Redirecting...', 'success');
            
            // Update UI and redirect
            checkAuthStatus();
            
            // Redirect to dashboard after 2 seconds
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 2000);
        } else {
            showMessage(messageDiv, data.error || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Network error. Please try again.', 'error');
        console.error('Login error:', error);
    }
}

// Handle Register
async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password') ? document.getElementById('confirm-password').value : password;
    const messageDiv = document.getElementById('register-message');
    
    // Validate inputs
    if (!username || !email || !password) {
        showMessage(messageDiv, 'Please fill in all fields', 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        showMessage(messageDiv, 'Passwords do not match', 'error');
        return;
    }
    
    try {
        const response = await fetch(API_BASE_URL + '/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok || response.status === 201) {
            showMessage(messageDiv, 'Registration successful! Redirecting to login...', 'success');
            
            // Redirect to login page after 2 seconds
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            showMessage(messageDiv, data.error || 'Registration failed', 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Network error. Please try again.', 'error');
        console.error('Registration error:', error);
    }
}

// Handle Logout
function handleLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('user_id');
    
    // Update UI and redirect to homepage
    checkAuthStatus();
    window.location.href = 'index.html';
}

// Show message helper
function showMessage(element, message, type = 'info') {
    if (!element) return;
    
    element.textContent = message;
    element.className = 'message ' + type;
    element.style.display = 'block';
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            element.style.display = 'none';
        }, 5000);
    }
}
