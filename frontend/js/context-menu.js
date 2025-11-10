// Context menu functionality

let contextMenuBlockId = null;

function showContextMenu(x, y, blockId) {
    const menu = document.getElementById('contextMenu');
    contextMenuBlockId = blockId;
    
    // Position menu at cursor
    menu.style.left = `${x}px`;
    menu.style.top = `${y}px`;
    menu.classList.add('show');
    
    // Close menu on outside click
    setTimeout(() => {
        document.addEventListener('click', closeContextMenu);
    }, 0);
}

function closeContextMenu() {
    const menu = document.getElementById('contextMenu');
    menu.classList.remove('show');
    document.removeEventListener('click', closeContextMenu);
}

async function changeBlockType(blockId, newType) {
    try {
        // Update block type via API
        await apiClient.updateBlock(blockId, null, newType);
        
        // Update DOM
        const blockElement = document.querySelector(`[data-block-id="${blockId}"]`);
        if (blockElement) {
            blockElement.dataset.type = newType;
        }
        
        // Update local data
        const block = currentBlocks.find(b => b.id === blockId);
        if (block) {
            block.block_type = newType;
        }
        
        showSaveIndicator('saved');
        
    } catch (error) {
        console.error('Error changing block type:', error);
        alert('Error changing block type: ' + error.message);
    }
}

// Initialize context menu listeners
document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.querySelectorAll('.context-menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.stopPropagation();
            const newType = item.dataset.type;
            if (contextMenuBlockId) {
                changeBlockType(contextMenuBlockId, newType);
            }
            closeContextMenu();
        });
    });
});
