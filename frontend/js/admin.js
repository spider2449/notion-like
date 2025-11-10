const API_BASE = '/api';

// Check authentication and admin status
const token = localStorage.getItem('token');
if (!token) {
    window.location.href = '/login.html';
}

let currentUser = null;

// Load initial data
async function init() {
    try {
        // Check if user is admin
        const response = await fetch(`${API_BASE}/account/profile`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            currentUser = await response.json();
            if (!currentUser.is_admin) {
                alert('Access denied. Admin privileges required.');
                window.location.href = '/app.html';
                return;
            }
            
            await loadStatistics();
            await loadUsers();
        } else {
            window.location.href = '/login.html';
        }
    } catch (error) {
        console.error('Error initializing admin panel:', error);
        alert('Error loading admin panel');
    }
}

async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE}/admin/statistics`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const stats = await response.json();
            document.getElementById('total-users').textContent = stats.total_users;
            document.getElementById('admin-users').textContent = stats.admin_users;
            document.getElementById('regular-users').textContent = stats.regular_users;
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE}/admin/users`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const data = await response.json();
            renderUsers(data.users);
        } else {
            showError('Failed to load users');
        }
    } catch (error) {
        console.error('Error loading users:', error);
        showError('Error loading users');
    }
}

function renderUsers(users) {
    const tbody = document.getElementById('users-tbody');
    
    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="no-data">No users found</td></tr>';
        return;
    }
    
    tbody.innerHTML = users.map(user => `
        <tr>
            <td>${user.id}</td>
            <td>${escapeHtml(user.username)}</td>
            <td>${escapeHtml(user.email)}</td>
            <td>
                <span class="role-badge ${user.is_admin ? 'admin' : 'user'}">
                    ${user.is_admin ? 'Admin' : 'User'}
                </span>
            </td>
            <td>${new Date(user.created_at).toLocaleDateString()}</td>
            <td class="actions">
                ${user.id !== currentUser.id ? `
                    <button onclick="toggleAdmin(${user.id}, ${!user.is_admin})" class="btn-small">
                        ${user.is_admin ? 'Remove Admin' : 'Make Admin'}
                    </button>
                    <button onclick="deleteUser(${user.id}, '${escapeHtml(user.username)}')" class="btn-small btn-danger">
                        Delete
                    </button>
                ` : '<span class="text-muted">Current User</span>'}
            </td>
        </tr>
    `).join('');
}

function showCreateUserModal() {
    document.getElementById('createUserModal').style.display = 'flex';
}

function closeCreateUserModal() {
    document.getElementById('createUserModal').style.display = 'none';
    document.getElementById('createUserForm').reset();
}

document.getElementById('createUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('new-username').value;
    const email = document.getElementById('new-email').value;
    const password = document.getElementById('new-password').value;
    const is_admin = document.getElementById('new-is-admin').checked;
    
    try {
        const response = await fetch(`${API_BASE}/admin/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ username, email, password, is_admin })
        });
        
        const data = await response.json();
        if (response.ok) {
            showSuccess('User created successfully');
            closeCreateUserModal();
            await loadStatistics();
            await loadUsers();
        } else {
            showError(data.error || 'Failed to create user');
        }
    } catch (error) {
        console.error('Error creating user:', error);
        showError('Error creating user');
    }
});

async function toggleAdmin(userId, makeAdmin) {
    if (!confirm(`Are you sure you want to ${makeAdmin ? 'grant admin privileges to' : 'remove admin privileges from'} this user?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/admin/users/${userId}/admin`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ is_admin: makeAdmin })
        });
        
        const data = await response.json();
        if (response.ok) {
            showSuccess('Admin status updated successfully');
            await loadStatistics();
            await loadUsers();
        } else {
            showError(data.error || 'Failed to update admin status');
        }
    } catch (error) {
        console.error('Error updating admin status:', error);
        showError('Error updating admin status');
    }
}

async function deleteUser(userId, username) {
    if (!confirm(`Are you sure you want to delete user "${username}"? This action cannot be undone and will delete all their documents.`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/admin/users/${userId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        if (response.ok) {
            showSuccess('User deleted successfully');
            await loadStatistics();
            await loadUsers();
        } else {
            showError(data.error || 'Failed to delete user');
        }
    } catch (error) {
        console.error('Error deleting user:', error);
        showError('Error deleting user');
    }
}

function goToApp() {
    window.location.href = '/app.html';
}

function showSuccess(message) {
    alert(message);
}

function showError(message) {
    alert('Error: ' + message);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('createUserModal');
    if (event.target === modal) {
        closeCreateUserModal();
    }
}

// Initialize on page load
init();
