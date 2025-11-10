// Main app initialization and event handlers

// Check authentication on load
document.addEventListener('DOMContentLoaded', () => {
    // Check if user is authenticated
    if (!apiClient.token) {
        window.location.href = 'login.html';
        return;
    }
    
    // Initialize app
    initializeApp();
});

async function initializeApp() {
    // Check if user is admin and show admin button
    await checkAdminStatus();
    
    // Load navigation tree
    await loadNavigationTree();
    
    // Set up event listeners
    setupEventListeners();
}

async function checkAdminStatus() {
    try {
        const response = await fetch('/api/account/profile', {
            headers: {
                'Authorization': `Bearer ${apiClient.token}`
            }
        });
        
        if (response.ok) {
            const profile = await response.json();
            if (profile.is_admin) {
                const adminBtn = document.getElementById('adminBtn');
                if (adminBtn) {
                    adminBtn.style.display = 'flex';
                }
            }
        }
    } catch (error) {
        console.error('Error checking admin status:', error);
    }
}

function setupEventListeners() {
    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
    
    // New document button
    const newDocBtn = document.getElementById('newDocBtn');
    if (newDocBtn) {
        newDocBtn.addEventListener('click', createNewDocument);
    }
    
    // New folder button
    const newFolderBtn = document.getElementById('newFolderBtn');
    if (newFolderBtn) {
        newFolderBtn.addEventListener('click', createNewFolder);
    }
    
    // Account settings button
    const accountBtn = document.getElementById('accountBtn');
    if (accountBtn) {
        accountBtn.addEventListener('click', () => {
            window.location.href = 'account.html';
        });
    }
    
    // Admin panel button
    const adminBtn = document.getElementById('adminBtn');
    if (adminBtn) {
        adminBtn.addEventListener('click', () => {
            window.location.href = 'admin.html';
        });
    }
}

async function handleLogout() {
    try {
        await apiClient.logout();
        apiClient.clearToken();
        window.location.href = 'login.html';
    } catch (error) {
        console.error('Error logging out:', error);
        // Clear token anyway and redirect
        apiClient.clearToken();
        window.location.href = 'login.html';
    }
}
