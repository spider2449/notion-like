const API_BASE = '/api';

// Check authentication
const token = localStorage.getItem('token');
if (!token) {
    window.location.href = '/login.html';
}

// Load profile information
async function loadProfile() {
    try {
        const response = await fetch(`${API_BASE}/account/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const profile = await response.json();
            document.getElementById('profile-info').innerHTML = `
                <p><strong>Username:</strong> ${profile.username}</p>
                <p><strong>Email:</strong> ${profile.email}</p>
                <p><strong>Member since:</strong> ${new Date(profile.created_at).toLocaleDateString()}</p>
            `;
        } else {
            showError('Failed to load profile');
        }
    } catch (error) {
        showError('Error loading profile');
    }
}

// Update username
document.getElementById('username-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('new-username').value;

    try {
        const response = await fetch(`${API_BASE}/account/username`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ username })
        });

        const data = await response.json();
        if (response.ok) {
            showSuccess('Username updated successfully');
            loadProfile();
            document.getElementById('username-form').reset();
        } else {
            showError(data.error || 'Failed to update username');
        }
    } catch (error) {
        showError('Error updating username');
    }
});

// Update email
document.getElementById('email-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('new-email').value;

    try {
        const response = await fetch(`${API_BASE}/account/email`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();
        if (response.ok) {
            showSuccess('Email updated successfully');
            loadProfile();
            document.getElementById('email-form').reset();
        } else {
            showError(data.error || 'Failed to update email');
        }
    } catch (error) {
        showError('Error updating email');
    }
});

// Change password
document.getElementById('password-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const current_password = document.getElementById('current-password').value;
    const new_password = document.getElementById('new-password').value;

    try {
        const response = await fetch(`${API_BASE}/account/password`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ current_password, new_password })
        });

        const data = await response.json();
        if (response.ok) {
            showSuccess('Password changed successfully');
            document.getElementById('password-form').reset();
        } else {
            showError(data.error || 'Failed to change password');
        }
    } catch (error) {
        showError('Error changing password');
    }
});

// Delete account
document.getElementById('delete-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!confirm('Are you absolutely sure? This action cannot be undone.')) {
        return;
    }

    const password = document.getElementById('delete-password').value;

    try {
        const response = await fetch(`${API_BASE}/account/delete`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ password })
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.removeItem('token');
            alert('Account deleted successfully');
            window.location.href = '/login.html';
        } else {
            showError(data.error || 'Failed to delete account');
        }
    } catch (error) {
        showError('Error deleting account');
    }
});

function goBack() {
    window.location.href = '/app.html';
}

function showSuccess(message) {
    alert(message);
}

function showError(message) {
    alert('Error: ' + message);
}

// Load profile on page load
loadProfile();
