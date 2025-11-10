from backend.repositories.document_repository import DocumentRepository
from backend.repositories.folder_repository import FolderRepository
from backend.utils.security import sanitize_input

class DocumentService:
    """Service for document and folder operations."""
    
    @staticmethod
    def get_document(document_id, user_id):
        """Get a single document by ID."""
        document = DocumentRepository.find_by_id(document_id)
        if not document:
            raise ValueError('Document not found')
        if document.user_id != user_id:
            raise PermissionError('Unauthorized access to document')
        return document
    
    @staticmethod
    def create_document(user_id, title, folder_id=None):
        """Create a new document with user ownership."""
        title = sanitize_input(title)
        if not title or len(title.strip()) == 0:
            raise ValueError('Document title is required')
        
        # Validate folder ownership if folder_id provided
        if folder_id:
            folder = FolderRepository.find_by_id(folder_id)
            if not folder or folder.user_id != user_id:
                raise ValueError('Invalid folder')
        
        return DocumentRepository.create(user_id, title, folder_id)
    
    @staticmethod
    def get_user_documents(user_id):
        """Get all documents and folders for a user in hierarchical structure."""
        documents = DocumentRepository.find_by_user(user_id)
        folders = FolderRepository.find_by_user(user_id)
        
        # Build hierarchical structure
        folder_dict = {f.id: {**f.to_dict(), 'children': [], 'documents': []} for f in folders}
        root_folders = []
        root_documents = []
        
        # Organize folders into hierarchy
        for folder in folders:
            if folder.parent_folder_id is None:
                root_folders.append(folder_dict[folder.id])
            elif folder.parent_folder_id in folder_dict:
                folder_dict[folder.parent_folder_id]['children'].append(folder_dict[folder.id])
        
        # Organize documents into folders or root
        for doc in documents:
            doc_dict = doc.to_dict()
            if doc.folder_id is None:
                root_documents.append(doc_dict)
            elif doc.folder_id in folder_dict:
                folder_dict[doc.folder_id]['documents'].append(doc_dict)
        
        return {
            'folders': root_folders,
            'documents': root_documents
        }
    
    @staticmethod
    def update_document(document_id, user_id, title=None, folder_id=None):
        """Update document with authorization check."""
        document = DocumentRepository.find_by_id(document_id)
        if not document:
            raise ValueError('Document not found')
        
        if document.user_id != user_id:
            raise PermissionError('Unauthorized')
        
        # Validate folder ownership if folder_id provided
        if folder_id:
            folder = FolderRepository.find_by_id(folder_id)
            if not folder or folder.user_id != user_id:
                raise ValueError('Invalid folder')
        
        return DocumentRepository.update(document_id, title, folder_id)
    
    @staticmethod
    def delete_document(document_id, user_id):
        """Delete document with authorization check (cascades to blocks)."""
        document = DocumentRepository.find_by_id(document_id)
        if not document:
            raise ValueError('Document not found')
        
        if document.user_id != user_id:
            raise PermissionError('Unauthorized')
        
        return DocumentRepository.delete(document_id)
    
    @staticmethod
    def create_folder(user_id, name, parent_folder_id=None):
        """Create a new folder with parent folder validation."""
        name = sanitize_input(name)
        if not name or len(name.strip()) == 0:
            raise ValueError('Folder name is required')
        
        # Validate parent folder ownership if parent_folder_id provided
        if parent_folder_id:
            parent = FolderRepository.find_by_id(parent_folder_id)
            if not parent or parent.user_id != user_id:
                raise ValueError('Invalid parent folder')
        
        return FolderRepository.create(user_id, name, parent_folder_id)
    
    @staticmethod
    def delete_folder(folder_id, user_id):
        """Delete folder with authorization check."""
        folder = FolderRepository.find_by_id(folder_id)
        if not folder:
            raise ValueError('Folder not found')
        
        if folder.user_id != user_id:
            raise PermissionError('Unauthorized')
        
        return FolderRepository.delete(folder_id)
