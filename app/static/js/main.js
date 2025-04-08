// Handle authentication
const API_URL = 'http://localhost:5000/api';

async function login(email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        if (data.token) {
            localStorage.setItem('token', data.token);
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Login failed:', error);
    }
}

async function register(username, email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });
        const data = await response.json();
        if (response.ok) {
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Registration failed:', error);
    }
}

// Article functions
async function getArticles() {
    try {
        const response = await fetch(`${API_URL}/articles`);
        const data = await response.json();
        return data.articles;
    } catch (error) {
        console.error('Failed to fetch articles:', error);
        return [];
    }
}