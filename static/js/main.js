// API functions
// Handle authentication
// Replace the hardcoded API_URL with a dynamic one that adapts to the current domain
const API_URL = window.location.origin + '/api';

async function getArticles() {
    try {
        // Add trailing slash to prevent 308 redirects
        const response = await fetch(`${API_URL}/articles/`);
        const data = await response.json();
        return data.articles;
    } catch (error) {
        console.error('Failed to fetch articles:', error);
        return [];
    }
}

// Add other functions as needed
// Use MutationObserver instead of DOMNodeInserted
function observeDOMChanges() {
    // This is a modern replacement for DOMNodeInserted
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'childList') {
                // Handle DOM changes here
                console.log('DOM changed');
            }
        });
    });
    
    // Start observing the document with the configured parameters
    observer.observe(document.body, { childList: true, subtree: true });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Initialize observers if needed
    // observeDOMChanges();
});

// Load articles on page load
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('articles-container');
    if (!container) return; // Skip if container doesn't exist

    const articles = await getArticles();
    
    if (articles && articles.length > 0) {
        articles.forEach(article => {
            const articleCard = document.createElement('div');
            articleCard.className = 'article-card p-6 rounded-lg shadow-lg';
            articleCard.innerHTML = `
                <h2 class="text-xl font-bold mb-2">${article.title}</h2>
                <p class="text-gray-600 mb-4">${article.content.substring(0, 150)}...</p>
                <div class="flex items-center">
                    <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">${article.category}</span>
                </div>
            `;
            container.appendChild(articleCard);
        });
    } else if (container) {
        container.innerHTML = `
            <div class="col-span-full text-center text-gray-500">
                <p>No articles found. Check back later!</p>
            </div>
        `;
    }
});