"""
Script to ingest documents into ChromaDB.
"""
import argparse
from document_processor import DocumentProcessor
from chroma_manager import ChromaManager


def main():
    parser = argparse.ArgumentParser(description='Ingest documents into ChromaDB')
    parser.add_argument(
        'folder_path',
        type=str,
        help='Path to folder containing text documents'
    )
    parser.add_argument(
        '--collection',
        type=str,
        default='documents',
        help='Name of ChromaDB collection (default: documents)'
    )
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=1000,
        help='Size of text chunks in characters (default: 1000)'
    )
    parser.add_argument(
        '--chunk-overlap',
        type=int,
        default=200,
        help='Overlap between chunks in characters (default: 200)'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset the collection before ingesting'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("DOCUMENT INGESTION")
    print("=" * 60)

    # Initialize document processor
    processor = DocumentProcessor(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    )

    # Process documents
    print(f"\nProcessing documents from: {args.folder_path}")
    chunks = processor.process_folder(args.folder_path)

    if not chunks:
        print("No documents found or processed. Exiting.")
        return

    # Initialize ChromaDB manager
    chroma = ChromaManager(collection_name=args.collection)

    # Reset collection if requested
    if args.reset:
        print("\nResetting collection...")
        chroma.reset_collection()

    # Add documents to ChromaDB
    print("\nAdding documents to ChromaDB...")
    chroma.add_documents(chunks)

    # Display statistics
    stats = chroma.get_collection_stats()
    print("\n" + "=" * 60)
    print("INGESTION COMPLETE")
    print("=" * 60)
    print(f"Collection: {stats['collection_name']}")
    print(f"Total chunks in database: {stats['total_chunks']}")
    print(f"Persist directory: {stats['persist_directory']}")


if __name__ == "__main__":
    main()
