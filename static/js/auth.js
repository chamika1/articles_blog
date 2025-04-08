// Remove the API_URL constant since we're using relative paths
document.addEventListener('DOMContentLoaded', () => {
    // Register form handler
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value.trim();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            
            try {
                const response = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username,
                        email,
                        password
                    })
                });

                const data = await response.json();
                
                if (response.ok) {
                    alert('Registration successful! Please login.');
                    window.location.href = '/login';
                } else {
                    throw new Error(data.message || 'Registration failed');
                }
            } catch (error) {
                console.error('Registration error:', error);
                alert(error.message || 'Registration failed. Please try again.');
            }
        });
    }

    // Login form handler
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email,
                        password
                    })
                });

                const data = await response.json();
                
                if (response.ok && data.token) {
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    window.location.href = '/';
                } else {
                    throw new Error(data.message || 'Login failed');
                }
            } catch (error) {
                console.error('Login error:', error);
                alert(error.message || 'Login failed. Please try again.');
            }
        });
    }
});

// Auth functions
// Remove the duplicate API_URL declaration and use the one from main.js
// If API_URL is not defined, define it here
if (typeof API_URL === 'undefined') {
    const API_URL = window.location.origin + '/api';
}

// Login function
function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    if (!email || !password) {
        alert('Please enter both email and password');
        return;
    }
    
    fetch(`${window.location.origin}/api/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            window.location.href = '/';
        } else {
            alert('Login failed. Please check your credentials.');
        }
    })
    .catch(error => {
        console.error('Login error:', error);
        alert('Login failed. Please try again.');
    });
}

// Register function
function handleRegister(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    if (!username || !email || !password) {
        alert('Please fill in all fields');
        return;
    }
    
    fetch(`${window.location.origin}/api/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.message === 'Registration successful') {
            alert('Registration successful! Please login.');
            window.location.href = '/login';
        } else {
            alert(data.message || 'Registration failed. Email might already be in use.');
        }
    })
    .catch(error => {
        console.error('Registration error:', error);
        alert('Registration failed. Please try again.');
    });
}