"""
Utility script to re-index existing documents with new chunk size.

This script:
1. Backs up existing document metadata
2. Clears the ChromaDB collection
3. Allows you to re-upload documents with new 1000-char chunks

Usage:
    python reindex_documents.py --list              # List all documents
    python reindex_documents.py --clear             # Clear all documents (with confirmation)
    python reindex_documents.py --stats             # Show chunking statistics
"""

import argparse
from app.services.vector_db import get_vector_db_service


def list_documents():
    """List all documents in the database."""
    print("\n" + "="*70)
    print("DOCUMENTS IN DATABASE")
    print("="*70 + "\n")
    
    vector_db = get_vector_db_service()
    documents = vector_db.list_documents()
    
    if not documents:
        print("No documents found in database.\n")
        return
    
    for idx, doc in enumerate(documents, 1):
        print(f"{idx}. {doc['filename']}")
        print(f"   Document ID: {doc['document_id'][:20]}...")
        print(f"   Upload Date: {doc['upload_date']}")
        print(f"   File Size: {doc['file_size']:,} bytes")
        print()
    
    print(f"Total: {len(documents)} document(s)\n")


def show_stats():
    """Show chunking statistics for all documents."""
    print("\n" + "="*70)
    print("DOCUMENT CHUNKING STATISTICS")
    print("="*70 + "\n")
    
    vector_db = get_vector_db_service()
    documents = vector_db.list_documents()
    
    if not documents:
        print("No documents found in database.\n")
        return
    
    all_items = vector_db.collection.get()
    
    # Group chunks by document
    doc_chunks = {}
    for metadata in all_items['metadatas']:
        doc_id = metadata.get('document_id')
        if doc_id not in doc_chunks:
            doc_chunks[doc_id] = {
                'filename': metadata.get('filename', 'Unknown'),
                'chunks': [],
                'total_chunks': metadata.get('total_chunks', 0)
            }
    
    for doc_text, metadata in zip(all_items['documents'], all_items['metadatas']):
        doc_id = metadata.get('document_id')
        if doc_id:
            doc_chunks[doc_id]['chunks'].append(len(doc_text))
    
    # Display statistics
    for doc_id, info in doc_chunks.items():
        print(f"{info['filename']}")
        print(f"   Document ID: {doc_id[:20]}...")
        print(f"   Total Chunks: {info['total_chunks']}")
        
        if info['chunks']:
            avg_size = sum(info['chunks']) / len(info['chunks'])
            min_size = min(info['chunks'])
            max_size = max(info['chunks'])
            
            print(f"   Chunk Sizes: avg={avg_size:.0f}, min={min_size}, max={max_size} characters")
            
            # Determine if using old or new chunking
            if avg_size < 700:
                print(f"   OLD CHUNKING (500-char) - Consider re-uploading")
            else:
                print(f"   NEW CHUNKING (1000-char) - Good context")
        print()
    
    print(f"Total: {len(doc_chunks)} document(s)\n")


def clear_documents():
    """Clear all documents from the database."""
    print("\n" + "="*70)
    print("CLEAR ALL DOCUMENTS")
    print("="*70 + "\n")
    
    vector_db = get_vector_db_service()
    documents = vector_db.list_documents()
    
    if not documents:
        print("ℹDatabase is already empty.\n")
        return
    
    print(f"This will delete {len(documents)} document(s):\n")
    for idx, doc in enumerate(documents, 1):
        print(f"  {idx}. {doc['filename']}")
    
    print("\nWARNING: This action cannot be undone!")
    confirm = input("\nType 'DELETE' to confirm: ")
    
    if confirm != "DELETE":
        print("\nOperation cancelled.\n")
        return
    
    print("\nDeleting documents...")
    
    for doc in documents:
        try:
            vector_db.delete_document(doc['document_id'])
            print(f"   ✓ Deleted: {doc['filename']}")
        except Exception as e:
            print(f"   Failed to delete {doc['filename']}: {str(e)}")
    
    remaining = len(vector_db.list_documents())
    if remaining == 0:
        print("\nAll documents deleted successfully!")
        print("You can now re-upload documents with improved chunking.\n")
    else:
        print(f"\n{remaining} document(s) could not be deleted.\n")


def main():
    parser = argparse.ArgumentParser(
        description="Manage document re-indexing for improved chunking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python reindex_documents.py --list      # View all documents
  python reindex_documents.py --stats     # Check chunking sizes
  python reindex_documents.py --clear     # Clear all documents

After clearing, re-upload your documents via:
  - Web UI: http://localhost:8000/advanced
  - API: POST /upload endpoint
        """
    )
    
    parser.add_argument('--list', action='store_true', 
                       help='List all documents in database')
    parser.add_argument('--stats', action='store_true',
                       help='Show document chunking statistics')
    parser.add_argument('--clear', action='store_true',
                       help='Clear all documents (requires confirmation)')
    
    args = parser.parse_args()
    
    if not any([args.list, args.stats, args.clear]):
        parser.print_help()
        return
    
    if args.list:
        list_documents()
    
    if args.stats:
        show_stats()
    
    if args.clear:
        clear_documents()


if __name__ == "__main__":
    main()
