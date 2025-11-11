// Enhanced editor functionality with slash commands and keyboard shortcuts

let currentBlocks = [];
let saveTimeouts = {};
let slashMenuVisible = false;
let slashMenuBlockId = null;
let selectedSlashIndex = 0;

async function loadDocument(documentId) {
    try {
        showLoading();
        currentDocumentId = documentId;
        
        // Fetch document details
        const docResponse = await apiClient.getDocument(documentId);
        
        // Fetch blocks
        const response = await apiClient.getBlocks(documentId);
        currentBlocks = response.blocks || [];
        
        // Render editor
        renderEditor(docResponse.document);
        
        // Update navigation active state
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
            if (item.dataset.docId == documentId) {
                item.classList.add('active');
            }
        });
        
        hideLoading();
    } catch (error) {
        console.error('Error loading document:', error);
        alert('Error loading document: ' + error.message);
        hideLoading();
    }
}

function renderEditor(doc) {
    const container = document.getElementById('editorContainer');
    container.innerHTML = '';
    
    // Create document title
    const titleInput = document.createElement('div');
    titleInput.className = 'document-title';
    titleInput.contentEditable = true;
    titleInput.textContent = doc.title;
    titleInput.addEventListener('input', () => {
        handleTitleChange(doc.id, titleInput.textContent);
    });
    titleInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            // Focus on first block or create one
            const firstBlock = container.querySelector('.block-content');
            if (firstBlock) {
                firstBlock.focus();
            } else {
                createNewBlock();
            }
        }
    });
    
    // Create blocks container
    const blocksContainer = document.createElement('div');
    blocksContainer.className = 'blocks-container';
    blocksContainer.id = 'blocksContainer';
    
    // Append to DOM first
    container.appendChild(titleInput);
    container.appendChild(blocksContainer);
    
    // Render blocks
    if (currentBlocks.length === 0) {
        // Create initial block without auto-focus
        createNewBlock(false);
    } else {
        currentBlocks.forEach(block => {
            blocksContainer.appendChild(createBlockElement(block));
        });
    }
    
    // Add save indicator
    if (!document.getElementById('saveIndicator')) {
        const saveIndicator = document.createElement('div');
        saveIndicator.id = 'saveIndicator';
        saveIndicator.className = 'save-indicator';
        document.body.appendChild(saveIndicator);
    }
}

function getPlaceholderText(blockType) {
    const placeholders = {
        'paragraph': "Type '/' for commands",
        'heading1': 'Heading 1',
        'heading2': 'Heading 2',
        'heading3': 'Heading 3',
        'bullet_list': 'List',
        'numbered_list': 'List',
        'code': 'Code',
        'quote': 'Quote',
        'callout': 'Callout',
        'divider': 'Divider'
    };
    return placeholders[blockType] || "Type '/' for commands";
}

function createBlockElement(block) {
    const blockDiv = document.createElement('div');
    blockDiv.className = 'block';
    blockDiv.dataset.blockId = block.id;
    blockDiv.dataset.type = block.block_type;
    blockDiv.draggable = true;
    
    // Add drag handle
    const handle = document.createElement('div');
    handle.className = 'block-handle';
    handle.textContent = '⋮⋮';
    handle.title = 'Click to change type, drag to reorder';
    
    // Click on handle to show type menu
    handle.addEventListener('click', (e) => {
        e.stopPropagation();
        showBlockTypeMenu(e.clientX, e.clientY, block.id);
    });
    
    const contentWrapper = document.createElement('div');
    contentWrapper.className = 'block-content-wrapper';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'block-content';
    
    // Handle special block types differently
    if (block.block_type === 'table') {
        contentDiv.contentEditable = false;
        renderTableContent(contentDiv, block);
    } else if (block.block_type === 'image') {
        contentDiv.contentEditable = false;
        renderImageContent(contentDiv, block);
    } else if (block.block_type === 'divider') {
        // Divider is just a visual element, no content needed
        contentDiv.contentEditable = false;
        contentDiv.innerHTML = '';
    } else {
        contentDiv.contentEditable = true;
        
        // Decode HTML entities for code blocks (in case old data has encoded content)
        let content = block.content;
        if (block.block_type === 'code' && content && content.includes('&')) {
            const textarea = document.createElement('textarea');
            textarea.innerHTML = content;
            content = textarea.value;
        }
        
        contentDiv.textContent = content;
        
        // Set placeholder based on block type
        contentDiv.setAttribute('data-placeholder', getPlaceholderText(block.block_type));
        
        // Add input listener for auto-save
        contentDiv.addEventListener('input', () => {
            handleBlockInput(block.id, contentDiv.textContent);
        });
        
        // Add keyboard shortcuts
        contentDiv.addEventListener('keydown', (e) => {
            handleBlockKeydown(e, block.id, contentDiv);
        });
        
        // Add keyup for slash command
        contentDiv.addEventListener('keyup', (e) => {
            handleSlashCommand(e, block.id, contentDiv);
        });
    }
    
    // Drag and drop handlers
    blockDiv.addEventListener('dragstart', handleDragStart);
    blockDiv.addEventListener('dragover', handleDragOver);
    blockDiv.addEventListener('drop', handleDrop);
    blockDiv.addEventListener('dragend', handleDragEnd);
    blockDiv.addEventListener('dragenter', handleDragEnter);
    blockDiv.addEventListener('dragleave', handleDragLeave);
    
    contentWrapper.appendChild(contentDiv);
    blockDiv.appendChild(handle);
    blockDiv.appendChild(contentWrapper);
    
    return blockDiv;
}

function handleBlockKeydown(e, blockId, contentDiv) {
    // Handle slash menu navigation
    if (slashMenuVisible) {
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            navigateSlashMenu(1);
            return;
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            navigateSlashMenu(-1);
            return;
        } else if (e.key === 'Enter') {
            e.preventDefault();
            selectSlashMenuItem();
            return;
        } else if (e.key === 'Escape') {
            hideSlashMenu();
            return;
        }
    }
    
    // Slash key - show slash menu (prevent default to avoid typing '/')
    if (e.key === '/' && contentDiv.textContent === '') {
        e.preventDefault();
        showSlashMenu(contentDiv, blockId);
        return;
    }
    
    // Enter key - create new block
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        createNewBlockAfter(blockId);
        return;
    }
    
    // Backspace on empty block - delete block
    if (e.key === 'Backspace' && contentDiv.textContent === '') {
        e.preventDefault();
        deleteBlockAndFocusPrevious(blockId);
        return;
    }
    
    // Tab - indent (future feature)
    if (e.key === 'Tab') {
        e.preventDefault();
        // Could implement indentation here
    }
}

function handleSlashCommand(e, blockId, contentDiv) {
    const text = contentDiv.textContent;
    
    // Hide menu if user starts typing something other than slash
    if (slashMenuVisible && text.length > 0) {
        hideSlashMenu();
    }
}

function showSlashMenu(contentDiv, blockId) {
    const menu = document.getElementById('slashMenu');
    const rect = contentDiv.getBoundingClientRect();
    
    menu.style.left = `${rect.left}px`;
    menu.style.top = `${rect.bottom + 5}px`;
    menu.classList.add('show');
    
    slashMenuVisible = true;
    slashMenuBlockId = blockId;
    selectedSlashIndex = 0;
    
    updateSlashMenuSelection();
}

function showBlockTypeMenu(x, y, blockId) {
    const menu = document.getElementById('slashMenu');
    
    menu.style.left = `${x}px`;
    menu.style.top = `${y}px`;
    menu.classList.add('show');
    
    slashMenuVisible = true;
    slashMenuBlockId = blockId;
    
    // Get current block type and select it
    const blockElement = document.querySelector(`[data-block-id="${blockId}"]`);
    const currentType = blockElement?.dataset.type || 'paragraph';
    
    const items = document.querySelectorAll('.slash-menu-item');
    selectedSlashIndex = 0;
    items.forEach((item, index) => {
        if (item.dataset.type === currentType) {
            selectedSlashIndex = index;
        }
    });
    
    updateSlashMenuSelection();
}

function hideSlashMenu() {
    const menu = document.getElementById('slashMenu');
    menu.classList.remove('show');
    slashMenuVisible = false;
    slashMenuBlockId = null;
}

function navigateSlashMenu(direction) {
    const items = document.querySelectorAll('.slash-menu-item');
    selectedSlashIndex = (selectedSlashIndex + direction + items.length) % items.length;
    updateSlashMenuSelection();
}

function updateSlashMenuSelection() {
    const items = document.querySelectorAll('.slash-menu-item');
    
    // Get current block type if menu is open
    let currentType = null;
    if (slashMenuBlockId) {
        const blockElement = document.querySelector(`[data-block-id="${slashMenuBlockId}"]`);
        currentType = blockElement?.dataset.type;
    }
    
    items.forEach((item, index) => {
        // Remove all classes first
        item.classList.remove('selected', 'current');
        
        // Add selected class for keyboard navigation
        if (index === selectedSlashIndex) {
            item.classList.add('selected');
            item.scrollIntoView({ block: 'nearest' });
        }
        
        // Add current class if this is the current block type
        if (currentType && item.dataset.type === currentType) {
            item.classList.add('current');
        }
    });
}

function selectSlashMenuItem() {
    const items = document.querySelectorAll('.slash-menu-item');
    const selectedItem = items[selectedSlashIndex];
    if (selectedItem) {
        const blockType = selectedItem.dataset.type;
        changeBlockType(slashMenuBlockId, blockType);
        
        const blockElement = document.querySelector(`[data-block-id="${slashMenuBlockId}"]`);
        const contentDiv = blockElement.querySelector('.block-content');
        
        hideSlashMenu();
        contentDiv.focus();
    }
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

function handleTitleChange(documentId, title) {
    if (saveTimeouts['title']) {
        clearTimeout(saveTimeouts['title']);
    }
    
    showSaveIndicator('saving');
    
    saveTimeouts['title'] = setTimeout(async () => {
        try {
            await apiClient.updateDocument(documentId, title);
            showSaveIndicator('saved');
            
            // Update navigation
            await loadNavigationTree();
        } catch (error) {
            console.error('Error saving title:', error);
            showSaveIndicator('error');
        }
    }, 1000);
}

async function createNewBlock(autoFocus = true) {
    if (!currentDocumentId) return;
    
    try {
        const response = await apiClient.createBlock(currentDocumentId);
        const block = response.block;
        currentBlocks.push(block);
        
        // Add block to DOM
        const blocksContainer = document.getElementById('blocksContainer');
        if (!blocksContainer) {
            console.error('Blocks container not found');
            return;
        }
        
        const blockElement = createBlockElement(block);
        blocksContainer.appendChild(blockElement);
        
        // Focus on new block if requested
        if (autoFocus) {
            const contentDiv = blockElement.querySelector('.block-content');
            contentDiv.focus();
        }
        
        return block;
        
    } catch (error) {
        console.error('Error creating block:', error);
        alert('Error creating block: ' + error.message);
    }
}

async function createNewBlockAfter(blockId) {
    if (!currentDocumentId) return;
    
    try {
        const response = await apiClient.createBlock(currentDocumentId);
        const newBlock = response.block;
        
        // Find index of current block
        const currentIndex = currentBlocks.findIndex(b => b.id === blockId);
        currentBlocks.splice(currentIndex + 1, 0, newBlock);
        
        // Add block to DOM after current block
        const currentBlockElement = document.querySelector(`[data-block-id="${blockId}"]`);
        const newBlockElement = createBlockElement(newBlock);
        currentBlockElement.after(newBlockElement);
        
        // Focus on new block
        const contentDiv = newBlockElement.querySelector('.block-content');
        contentDiv.focus();
        
    } catch (error) {
        console.error('Error creating block:', error);
    }
}

async function deleteBlockAndFocusPrevious(blockId) {
    const blockIndex = currentBlocks.findIndex(b => b.id === blockId);
    
    // Don't delete if it's the only block
    if (currentBlocks.length === 1) {
        return;
    }
    
    try {
        await apiClient.deleteBlock(blockId);
        
        // Remove from DOM
        const blockElement = document.querySelector(`[data-block-id="${blockId}"]`);
        const previousBlock = blockElement.previousElementSibling;
        
        if (blockElement) {
            blockElement.remove();
        }
        
        // Remove from local data
        currentBlocks = currentBlocks.filter(b => b.id !== blockId);
        
        // Focus on previous block
        if (previousBlock) {
            const contentDiv = previousBlock.querySelector('.block-content');
            if (contentDiv) {
                contentDiv.focus();
                // Move cursor to end
                const range = document.createRange();
                const sel = window.getSelection();
                range.selectNodeContents(contentDiv);
                range.collapse(false);
                sel.removeAllRanges();
                sel.addRange(range);
            }
        }
        
    } catch (error) {
        console.error('Error deleting block:', error);
    }
}

function renderTableContent(contentDiv, block) {
    // Parse table data from content (stored as JSON)
    let tableData;
    try {
        tableData = block.content ? JSON.parse(block.content) : { rows: 3, cols: 3, data: {} };
    } catch (e) {
        // Default table structure
        tableData = { rows: 3, cols: 3, data: {} };
    }
    
    const tableWrapper = document.createElement('div');
    tableWrapper.className = 'table-wrapper';
    
    const table = document.createElement('table');
    
    // Create header row
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    for (let col = 0; col < tableData.cols; col++) {
        const th = document.createElement('th');
        th.contentEditable = true;
        th.textContent = tableData.data[`0-${col}`] || `Column ${col + 1}`;
        th.addEventListener('input', () => {
            saveTableData(block.id, tableWrapper);
        });
        headerRow.appendChild(th);
    }
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Create body rows
    const tbody = document.createElement('tbody');
    for (let row = 1; row < tableData.rows; row++) {
        const tr = document.createElement('tr');
        for (let col = 0; col < tableData.cols; col++) {
            const td = document.createElement('td');
            td.contentEditable = true;
            td.textContent = tableData.data[`${row}-${col}`] || '';
            td.addEventListener('input', () => {
                saveTableData(block.id, tableWrapper);
            });
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    
    tableWrapper.appendChild(table);
    
    // Add table controls
    const controls = document.createElement('div');
    controls.className = 'table-controls';
    
    const addRowBtn = document.createElement('button');
    addRowBtn.className = 'table-control-btn';
    addRowBtn.textContent = '+ Add Row';
    addRowBtn.onclick = (e) => {
        e.preventDefault();
        addTableRow(block.id, tableWrapper);
    };
    
    const addColBtn = document.createElement('button');
    addColBtn.className = 'table-control-btn';
    addColBtn.textContent = '+ Add Column';
    addColBtn.onclick = (e) => {
        e.preventDefault();
        addTableColumn(block.id, tableWrapper);
    };
    
    const deleteRowBtn = document.createElement('button');
    deleteRowBtn.className = 'table-control-btn table-control-delete';
    deleteRowBtn.textContent = '− Delete Row';
    deleteRowBtn.onclick = (e) => {
        e.preventDefault();
        deleteTableRow(block.id, tableWrapper);
    };
    
    const deleteColBtn = document.createElement('button');
    deleteColBtn.className = 'table-control-btn table-control-delete';
    deleteColBtn.textContent = '− Delete Column';
    deleteColBtn.onclick = (e) => {
        e.preventDefault();
        deleteTableColumn(block.id, tableWrapper);
    };
    
    controls.appendChild(addRowBtn);
    controls.appendChild(addColBtn);
    controls.appendChild(deleteRowBtn);
    controls.appendChild(deleteColBtn);
    
    tableWrapper.appendChild(controls);
    contentDiv.appendChild(tableWrapper);
}

function saveTableData(blockId, tableWrapper) {
    // Extract data from table
    const table = tableWrapper.querySelector('table');
    const data = {};
    let rows = 0;
    let cols = 0;
    
    // Get header data
    const headers = table.querySelectorAll('thead th');
    cols = headers.length;
    headers.forEach((th, col) => {
        data[`0-${col}`] = th.textContent;
    });
    rows++;
    
    // Get body data
    const bodyRows = table.querySelectorAll('tbody tr');
    bodyRows.forEach((tr, rowIndex) => {
        const cells = tr.querySelectorAll('td');
        cells.forEach((td, col) => {
            data[`${rowIndex + 1}-${col}`] = td.textContent;
        });
        rows++;
    });
    
    const tableData = { rows, cols, data };
    const content = JSON.stringify(tableData);
    
    // Save with debounce
    handleBlockInput(blockId, content);
}

function addTableRow(blockId, tableWrapper) {
    const table = tableWrapper.querySelector('table');
    const tbody = table.querySelector('tbody');
    const cols = table.querySelectorAll('thead th').length;
    
    const tr = document.createElement('tr');
    for (let col = 0; col < cols; col++) {
        const td = document.createElement('td');
        td.contentEditable = true;
        td.textContent = '';
        td.addEventListener('input', () => {
            saveTableData(blockId, tableWrapper);
        });
        tr.appendChild(td);
    }
    tbody.appendChild(tr);
    
    saveTableData(blockId, tableWrapper);
}

function addTableColumn(blockId, tableWrapper) {
    const table = tableWrapper.querySelector('table');
    
    // Add header cell
    const headerRow = table.querySelector('thead tr');
    const th = document.createElement('th');
    th.contentEditable = true;
    th.textContent = `Column ${headerRow.children.length + 1}`;
    th.addEventListener('input', () => {
        saveTableData(blockId, tableWrapper);
    });
    headerRow.appendChild(th);
    
    // Add cell to each body row
    const bodyRows = table.querySelectorAll('tbody tr');
    bodyRows.forEach(tr => {
        const td = document.createElement('td');
        td.contentEditable = true;
        td.textContent = '';
        td.addEventListener('input', () => {
            saveTableData(blockId, tableWrapper);
        });
        tr.appendChild(td);
    });
    
    saveTableData(blockId, tableWrapper);
}

function deleteTableRow(blockId, tableWrapper) {
    const table = tableWrapper.querySelector('table');
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');
    
    // Don't delete if only one row left
    if (rows.length <= 1) {
        alert('Table must have at least one data row');
        return;
    }
    
    // Delete last row
    rows[rows.length - 1].remove();
    saveTableData(blockId, tableWrapper);
}

function deleteTableColumn(blockId, tableWrapper) {
    const table = tableWrapper.querySelector('table');
    const headerRow = table.querySelector('thead tr');
    const cols = headerRow.children.length;
    
    // Don't delete if only one column left
    if (cols <= 1) {
        alert('Table must have at least one column');
        return;
    }
    
    // Delete last column from header
    headerRow.removeChild(headerRow.lastChild);
    
    // Delete last column from each body row
    const bodyRows = table.querySelectorAll('tbody tr');
    bodyRows.forEach(tr => {
        if (tr.lastChild) {
            tr.removeChild(tr.lastChild);
        }
    });
    
    saveTableData(blockId, tableWrapper);
}

function renderImageContent(contentDiv, block) {
    const imageWrapper = document.createElement('div');
    imageWrapper.className = 'image-wrapper';
    
    // Parse image data from content (stored as JSON)
    let imageData;
    try {
        // Handle empty or whitespace content
        if (!block.content || block.content.trim() === '') {
            imageData = { url: '', caption: '' };
        } else {
            // Decode HTML entities if present
            let content = block.content;
            if (content.includes('&quot;')) {
                const textarea = document.createElement('textarea');
                textarea.innerHTML = content;
                content = textarea.value;
            }
            imageData = JSON.parse(content);
        }
    } catch (e) {
        console.error('Failed to parse image content:', e);
        imageData = { url: '', caption: '' };
    }
    
    if (imageData.url) {
        // Display image
        const img = document.createElement('img');
        img.src = imageData.url;
        img.alt = imageData.caption || 'Image';
        img.className = 'block-image';
        imageWrapper.appendChild(img);
        
        // Caption
        const caption = document.createElement('div');
        caption.className = 'image-caption';
        caption.contentEditable = true;
        caption.textContent = imageData.caption || '';
        caption.placeholder = 'Add a caption...';
        caption.addEventListener('input', () => {
            imageData.caption = caption.textContent;
            handleBlockInput(block.id, JSON.stringify(imageData));
        });
        imageWrapper.appendChild(caption);
        
        // Change image button
        const changeBtn = document.createElement('button');
        changeBtn.className = 'image-change-btn';
        changeBtn.textContent = 'Change Image';
        changeBtn.onclick = (e) => {
            e.preventDefault();
            triggerImageUpload(block.id);
        };
        imageWrapper.appendChild(changeBtn);
    } else {
        // Upload interface
        const uploadArea = document.createElement('div');
        uploadArea.className = 'image-upload-area';
        uploadArea.innerHTML = `
            <div class="upload-prompt">
                <span class="upload-icon">📷</span>
                <p>Click to upload an image</p>
                <p class="upload-hint">or paste an image URL</p>
            </div>
        `;
        
        uploadArea.onclick = () => {
            triggerImageUpload(block.id);
        };
        
        // URL input
        const urlInput = document.createElement('input');
        urlInput.type = 'text';
        urlInput.className = 'image-url-input';
        urlInput.placeholder = 'Paste image URL...';
        urlInput.addEventListener('keydown', async (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const url = urlInput.value.trim();
                if (url) {
                    await saveImageUrl(block.id, url);
                }
            }
        });
        
        imageWrapper.appendChild(uploadArea);
        imageWrapper.appendChild(urlInput);
    }
    
    contentDiv.appendChild(imageWrapper);
}

function triggerImageUpload(blockId) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (file) {
            await uploadImage(blockId, file);
        }
    };
    input.click();
}

async function uploadImage(blockId, file) {
    try {
        showSaveIndicator('saving');
        
        const formData = new FormData();
        formData.append('image', file);
        
        const response = await fetch('/api/upload/image', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Upload failed');
        }
        
        const data = await response.json();
        await saveImageUrl(blockId, data.url);
        
    } catch (error) {
        console.error('Error uploading image:', error);
        showSaveIndicator('error');
        alert('Failed to upload image: ' + error.message);
    }
}

async function saveImageUrl(blockId, url) {
    try {
        const imageData = { url, caption: '' };
        const content = JSON.stringify(imageData);
        
        await apiClient.updateBlock(blockId, content);
        
        // Update local data
        const block = currentBlocks.find(b => b.id === blockId);
        if (block) {
            block.content = content;
        }
        
        // Re-render the block
        const blockElement = document.querySelector(`[data-block-id="${blockId}"]`);
        if (blockElement && block) {
            const newBlockElement = createBlockElement(block);
            blockElement.replaceWith(newBlockElement);
        }
        
        showSaveIndicator('saved');
        
    } catch (error) {
        console.error('Error saving image:', error);
        showSaveIndicator('error');
        alert('Failed to save image: ' + error.message);
    }
}

async function changeBlockType(blockId, newType) {
    try {
        const block = currentBlocks.find(b => b.id === blockId);
        const oldType = block?.block_type;
        
        // Initialize content for special block types
        let newContent = null;
        if (newType === 'table' && oldType !== 'table') {
            const defaultTable = {
                rows: 3,
                cols: 3,
                data: {
                    '0-0': 'Column 1',
                    '0-1': 'Column 2',
                    '0-2': 'Column 3'
                }
            };
            newContent = JSON.stringify(defaultTable);
        } else if (newType === 'image' && oldType !== 'image') {
            const defaultImage = { url: '', caption: '' };
            newContent = JSON.stringify(defaultImage);
        }
        
        // Update block type via API
        await apiClient.updateBlock(blockId, newContent, newType);
        
        // Update local data
        if (block) {
            block.block_type = newType;
            if (newContent !== null) {
                block.content = newContent;
            }
        }
        
        // Re-render the block
        const blockElement = document.querySelector(`[data-block-id="${blockId}"]`);
        if (blockElement && block) {
            const newBlockElement = createBlockElement(block);
            blockElement.replaceWith(newBlockElement);
        }
        
        showSaveIndicator('saved');
        
    } catch (error) {
        console.error('Error changing block type:', error);
        alert('Error changing block type: ' + error.message);
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
        indicator.textContent = '✓ Saved';
    } else if (status === 'error') {
        indicator.textContent = '✗ Error';
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

// Initialize slash menu click handlers
document.addEventListener('DOMContentLoaded', () => {
    const slashMenuItems = document.querySelectorAll('.slash-menu-item');
    slashMenuItems.forEach((item, index) => {
        item.addEventListener('click', (e) => {
            e.stopPropagation();
            selectedSlashIndex = index;
            selectSlashMenuItem();
        });
    });
    
    // Close slash menu on outside click
    document.addEventListener('click', (e) => {
        if (slashMenuVisible && !e.target.closest('.slash-menu') && !e.target.closest('.block-handle')) {
            hideSlashMenu();
        }
    });
});


// Drag and Drop functionality
let draggedBlock = null;

function handleDragStart(e) {
    draggedBlock = this;
    this.style.opacity = '0.4';
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    return false;
}

function handleDragEnter(e) {
    if (this !== draggedBlock) {
        this.classList.add('drag-over');
    }
}

function handleDragLeave(e) {
    this.classList.remove('drag-over');
}

function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    if (draggedBlock !== this) {
        // Get the container
        const container = document.getElementById('blocksContainer');
        const allBlocks = Array.from(container.querySelectorAll('.block'));
        
        const draggedIndex = allBlocks.indexOf(draggedBlock);
        const targetIndex = allBlocks.indexOf(this);
        
        // Reorder in DOM
        if (draggedIndex < targetIndex) {
            this.parentNode.insertBefore(draggedBlock, this.nextSibling);
        } else {
            this.parentNode.insertBefore(draggedBlock, this);
        }
        
        // Update local blocks array
        const draggedBlockId = parseInt(draggedBlock.dataset.blockId);
        const draggedBlockData = currentBlocks.find(b => b.id === draggedBlockId);
        const draggedBlockIndex = currentBlocks.indexOf(draggedBlockData);
        
        currentBlocks.splice(draggedBlockIndex, 1);
        
        const targetBlockId = parseInt(this.dataset.blockId);
        const targetBlockData = currentBlocks.find(b => b.id === targetBlockId);
        let newIndex = currentBlocks.indexOf(targetBlockData);
        
        if (draggedIndex < targetIndex) {
            newIndex++;
        }
        
        currentBlocks.splice(newIndex, 0, draggedBlockData);
        
        // Update order_index for all blocks
        currentBlocks.forEach((block, index) => {
            block.order_index = index;
        });
        
        // Save new order to backend
        saveBlockOrder();
    }
    
    this.classList.remove('drag-over');
    return false;
}

function handleDragEnd(e) {
    this.style.opacity = '1';
    
    // Remove drag-over class from all blocks
    document.querySelectorAll('.block').forEach(block => {
        block.classList.remove('drag-over');
    });
}

async function saveBlockOrder() {
    if (!currentDocumentId) return;
    
    try {
        const blockOrder = currentBlocks.map((block, index) => ({
            id: block.id,
            order_index: index
        }));
        
        await apiClient.reorderBlocks(currentDocumentId, blockOrder);
        showSaveIndicator('saved');
    } catch (error) {
        console.error('Error saving block order:', error);
        showSaveIndicator('error');
    }
}
