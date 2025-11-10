// Navigation panel functionality

let currentDocumentId = null;
let navigationData = null;
let openFolders = new Set(); // Track which folders are open

async function loadNavigationTree() {
    try {
        showLoading();
        const data = await apiClient.getDocuments();
        navigationData = data;
        renderNavigationTree(data);
        hideLoading();
    } catch (error) {
        console.error('Error loading navigation:', error);
        hideLoading();
    }
}

function renderNavigationTree(data) {
    const container = document.getElementById('navigationTree');
    container.innerHTML = '';
    
    // Render folders
    data.folders.forEach(folder => {
        container.appendChild(createFolderElement(folder));
    });
    
    // Render root documents
    data.documents.forEach(doc => {
        container.appendChild(createDocumentElement(doc));
    });
}

function createFolderElement(folder, level = 0) {
    const folderDiv = document.createElement('div');
    folderDiv.className = 'folder-item';
    folderDiv.style.marginLeft = `${level * 10}px`;
    
    const folderHeader = document.createElement('div');
    folderHeader.className = 'nav-item';
    folderHeader.dataset.folderId = folder.id;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'nav-item-content';
    
    const toggle = document.createElement('span');
    toggle.className = 'folder-toggle';
    toggle.textContent = '▶';
    
    const icon = document.createElement('span');
    icon.className = 'nav-item-icon';
    icon.textContent = '📁';
    
    const name = document.createElement('span');
    name.className = 'nav-item-name';
    name.textContent = folder.name;
    
    contentDiv.appendChild(toggle);
    contentDiv.appendChild(icon);
    contentDiv.appendChild(name);
    
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'nav-item-delete';
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = (e) => {
        e.stopPropagation();
        deleteFolder(folder.id);
    };
    
    folderHeader.appendChild(contentDiv);
    folderHeader.appendChild(deleteBtn);
    folderDiv.appendChild(folderHeader);
    
    // Make folder a drop target
    folderHeader.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        folderHeader.classList.add('drag-over');
    });
    
    folderHeader.addEventListener('dragleave', (e) => {
        e.stopPropagation();
        folderHeader.classList.remove('drag-over');
    });
    
    folderHeader.addEventListener('drop', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        folderHeader.classList.remove('drag-over');
        
        const docId = e.dataTransfer.getData('text/plain');
        if (docId) {
            await moveDocumentToFolder(parseInt(docId), folder.id);
        }
    });
    
    // Create children container
    const childrenDiv = document.createElement('div');
    childrenDiv.className = 'folder-children';
    
    // Check if this folder was previously open
    const isOpen = openFolders.has(folder.id);
    childrenDiv.style.display = isOpen ? 'block' : 'none';
    toggle.textContent = isOpen ? '▼' : '▶';
    
    // Add child folders
    if (folder.children) {
        folder.children.forEach(child => {
            childrenDiv.appendChild(createFolderElement(child, level + 1));
        });
    }
    
    // Add documents in folder
    if (folder.documents) {
        folder.documents.forEach(doc => {
            childrenDiv.appendChild(createDocumentElement(doc, level + 1));
        });
    }
    
    folderDiv.appendChild(childrenDiv);
    
    // Toggle folder
    toggle.onclick = (e) => {
        e.stopPropagation();
        const isOpen = childrenDiv.style.display === 'block';
        childrenDiv.style.display = isOpen ? 'none' : 'block';
        toggle.textContent = isOpen ? '▶' : '▼';
        
        // Update open folders state
        if (isOpen) {
            openFolders.delete(folder.id);
        } else {
            openFolders.add(folder.id);
        }
    };
    
    return folderDiv;
}

function createDocumentElement(doc, level = 0) {
    const docDiv = document.createElement('div');
    docDiv.className = 'nav-item';
    docDiv.dataset.docId = doc.id;
    docDiv.style.marginLeft = `${level * 10}px`;
    docDiv.draggable = true;
    
    if (currentDocumentId === doc.id) {
        docDiv.classList.add('active');
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'nav-item-content';
    
    const icon = document.createElement('span');
    icon.className = 'nav-item-icon';
    icon.textContent = '📄';
    
    const name = document.createElement('span');
    name.className = 'nav-item-name';
    name.textContent = doc.title;
    
    contentDiv.appendChild(icon);
    contentDiv.appendChild(name);
    
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'nav-item-delete';
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = (e) => {
        e.stopPropagation();
        deleteDocument(doc.id);
    };
    
    docDiv.appendChild(contentDiv);
    docDiv.appendChild(deleteBtn);
    
    docDiv.onclick = () => {
        loadDocument(doc.id);
    };
    
    // Drag and drop handlers
    docDiv.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', doc.id);
        docDiv.classList.add('dragging');
    });
    
    docDiv.addEventListener('dragend', (e) => {
        docDiv.classList.remove('dragging');
    });
    
    return docDiv;
}

async function createNewDocument() {
    const title = prompt('Enter document title:');
    if (!title) return;
    
    try {
        showLoading();
        await apiClient.createDocument(title);
        await loadNavigationTree();
        hideLoading();
    } catch (error) {
        alert('Error creating document: ' + error.message);
        hideLoading();
    }
}

async function createNewFolder() {
    const name = prompt('Enter folder name:');
    if (!name) return;
    
    try {
        showLoading();
        await apiClient.createFolder(name);
        await loadNavigationTree();
        hideLoading();
    } catch (error) {
        alert('Error creating folder: ' + error.message);
        hideLoading();
    }
}

async function deleteDocument(documentId) {
    if (!confirm('Are you sure you want to delete this document?')) return;
    
    try {
        showLoading();
        await apiClient.deleteDocument(documentId);
        if (currentDocumentId === documentId) {
            currentDocumentId = null;
            showEditorPlaceholder();
        }
        await loadNavigationTree();
        hideLoading();
    } catch (error) {
        alert('Error deleting document: ' + error.message);
        hideLoading();
    }
}

async function deleteFolder(folderId) {
    if (!confirm('Are you sure you want to delete this folder? All contents will be deleted.')) return;
    
    try {
        showLoading();
        await apiClient.deleteFolder(folderId);
        await loadNavigationTree();
        hideLoading();
    } catch (error) {
        alert('Error deleting folder: ' + error.message);
        hideLoading();
    }
}

function showLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.classList.add('show');
    }
}

function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.classList.remove('show');
    }
}

async function moveDocumentToFolder(documentId, folderId) {
    try {
        showLoading();
        await apiClient.moveDocumentToFolder(documentId, folderId);
        await loadNavigationTree();
        hideLoading();
    } catch (error) {
        alert('Error moving document: ' + error.message);
        hideLoading();
    }
}
