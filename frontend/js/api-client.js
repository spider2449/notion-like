// API Client for making HTTP requests
const API_BASE_URL = 'http://localhost:5000/api';

class ApiClient {
    constructor() {
        this.token = localStorage.getItem('token');
    }
    
    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }
    
    clearToken() {
        this.token = null;
        localStorage.removeItem('token');
    }
    
    getAuthHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        return headers;
    }
    
    async request(method, endpoint, data = null) {
        const options = {
            method: method,
            headers: this.getAuthHeaders()
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
            const responseData = await response.json();
            
            // Handle 401 errors (authentication failures)
            if (response.status === 401) {
                this.clearToken();
                if (window.location.pathname !== '/frontend/html/login.html') {
                    window.location.href = 'login.html';
                }
                throw new Error(responseData.error || 'Authentication required');
            }
            
            if (!response.ok) {
                throw new Error(responseData.error || 'Request failed');
            }
            
            return responseData;
        } catch (error) {
            if (error.message === 'Failed to fetch') {
                throw new Error('Connection error. Please check your internet.');
            }
            throw error;
        }
    }
    
    // Auth endpoints
    async register(username, email, password) {
        return this.request('POST', '/auth/register', { username, email, password });
    }
    
    async login(username, password) {
        return this.request('POST', '/auth/login', { username, password });
    }
    
    async logout() {
        return this.request('POST', '/auth/logout');
    }
    
    // Document endpoints
    async getDocuments() {
        return this.request('GET', '/documents');
    }
    
    async getDocument(documentId) {
        return this.request('GET', `/documents/${documentId}`);
    }
    
    async createDocument(title, folderId = null) {
        return this.request('POST', '/documents', { title, folder_id: folderId });
    }
    
    async updateDocument(documentId, title, folderId = null) {
        return this.request('PUT', `/documents/${documentId}`, { title, folder_id: folderId });
    }
    
    async deleteDocument(documentId) {
        return this.request('DELETE', `/documents/${documentId}`);
    }
    
    async moveDocumentToFolder(documentId, folderId) {
        return this.request('PUT', `/documents/${documentId}`, { folder_id: folderId });
    }
    
    // Folder endpoints
    async createFolder(name, parentFolderId = null) {
        return this.request('POST', '/folders', { name, parent_folder_id: parentFolderId });
    }
    
    async deleteFolder(folderId) {
        return this.request('DELETE', `/folders/${folderId}`);
    }
    
    // Block endpoints
    async getBlocks(documentId) {
        return this.request('GET', `/documents/${documentId}/blocks`);
    }
    
    async createBlock(documentId, content = '', blockType = 'paragraph') {
        return this.request('POST', '/blocks', { document_id: documentId, content, block_type: blockType });
    }
    
    async updateBlock(blockId, content = null, blockType = null) {
        const data = {};
        if (content !== null) data.content = content;
        if (blockType !== null) data.block_type = blockType;
        return this.request('PUT', `/blocks/${blockId}`, data);
    }
    
    async deleteBlock(blockId) {
        return this.request('DELETE', `/blocks/${blockId}`);
    }
    
    async reorderBlocks(documentId, blocks) {
        return this.request('PUT', `/documents/${documentId}/blocks/reorder`, { blocks });
    }
}

// Create global instance
const apiClient = new ApiClient();
