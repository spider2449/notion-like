// Editor functionality

let currentBlocks = [];
let saveTimeouts = {};

async function loadDocument(documentId) {
    try {
        showLoading();
        currentDocumentId = documentId;
        
        // Fetch blocks
        const response = await apiClient.getBlocks(documentId);
        currentBlocks = response.blocks;
        
        // Render editor
        renderEditor();
        
        // Update navigation active state
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        hideLoading();
    } catch (error) {
        console.error('Error loading document:', error);
        alert('Error loading document: ' + error.message);
        hideLoading();
    }
}

function renderEditor() {
    const container = document.getElementById('editorContainer');
    container.innerHTML = '';
    
    // Create blocks container
    const blocksContainer = document.createElement('div');
    blocksContainer.className = 'blocks-container';
    blocksContainer.id = 'blocksContainer';
    
    // Render blocks
    currentBlocks.forEach(block => {
        blocksContainer.appendChild(createBlockElement(block));
    });
    
    // Add new block button
    const addBtn = document.createElement('button');
    addBtn.className = 'btn-add-block';
    addBtn.textContent = '+ Add Block';
    addBtn.onclick = createNewBlock;
    
    container.appendChild(blocksContainer);
    container.appendChild(addBtn);
    
    // Add save indicator
    if (!document.getElementById('saveIndicator')) {
        const saveIndicator = document.createElement('div');
        saveIndicator.id = 'saveIndicator';
        saveIndicator.className = 'save-indicator';
        document.body.appendChild(saveIndicator);
    }
}

function createBlockElement(block) {
    const blockDiv = document.createElement('div');
    blockDiv.className = 'block';
    blockDiv.dataset.blockId = block.id;
    blockDiv.dataset.type = block.block_type;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'block-content';
    contentDiv.contentEditable = true;
    contentDiv.textContent = block.content;
    
    // Add input listener for auto-save
    contentDiv.addEventListener('input', () => {
        handleBlockInput(block.id, contentDiv.textContent);
    });
    
    // Add right-click listener for context menu
    blockDiv.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        showContextMenu(e.clientX, e.clientY, block.id);
    });
    
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'block-delete';
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = () => deleteBlock(block.id);
    
    blockDiv.appendChild(contentDiv);
    blockDiv.appendChild(deleteBtn);
    
    return blockDiv;
}

function handleBlockInput(blockId, content) {
    // Clear existing timeout
    if (saveTimeouts[blockId]) {
        clearTimeout(saveTimeouts[blockId]);
    }
    
    // Show saving indicator
    showSaveIndicator('saving');
    
    // Set new timeout for auto-save (1 second debounce)
    saveTimeouts[blockId] = setTimeout(async () => {
        try {
            await apiClient.updateBlock(blockId, content);
            showSaveIndicator('saved');
            
            // Update local block data
            const block = currentBlocks.find(b => b.id === blockId);
            if (block) {
                block.content = content;
            }
        } catch (error) {
            console.error('Error saving block:', error);
            showSaveIndicator('error');
        }
    }, 1000);
}

async function createNewBlock() {
    if (!currentDocumentId) return;
    
    try {
        const response = await apiClient.createBlock(currentDocumentId);
        currentBlocks.push(response.block);
        
        // Add block to DOM
        const blocksContainer = document.getElementById('blocksContainer');
        const blockElement = createBlockElement(response.block);
        blocksContainer.appendChild(blockElement);
        
        // Focus on new block
        const contentDiv = blockElement.querySelector('.block-content');
        contentDiv.focus();
        
    } catch (error) {
        console.error('Error creating block:', error);
        alert('Error creating block: ' + error.message);
    }
}

async function deleteBlock(blockId) {
    try {
        await apiClient.deleteBlock(blockId);
        
        // Remove from DOM
        const blockElement = document.querySelector(`[data-block-id="${blockId}"]`);
        if (blockElement) {
            blockElement.remove();
        }
        
        // Remove from local data
        currentBlocks = currentBlocks.filter(b => b.id !== blockId);
        
    } catch (error) {
        console.error('Error deleting block:', error);
        alert('Error deleting block: ' + error.message);
    }
}

function showSaveIndicator(status) {
    const indicator = document.getElementById('saveIndicator');
    if (!indicator) return;
    
    indicator.classList.remove('saving', 'saved', 'error');
    indicator.classList.add(status);
    
    if (status === 'saving') {
        indicator.textContent = 'Saving...';
    } else if (status === 'saved') {
        indicator.textContent = 'Saved';
    } else if (status === 'error') {
        indicator.textContent = 'Error saving';
    }
    
    indicator.classList.add('show');
    
    // Hide after 2 seconds
    setTimeout(() => {
        indicator.classList.remove('show');
    }, 2000);
}

function showEditorPlaceholder() {
    const container = document.getElementById('editorContainer');
    container.innerHTML = `
        <div class="editor-placeholder">
            <h2>Select a document to start editing</h2>
            <p>Choose a document from the sidebar or create a new one</p>
        </div>
    `;
}
