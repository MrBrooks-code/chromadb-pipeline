"""
Example usage of the RAG pipeline.
This script demonstrates how to use the document processor and ChromaDB manager programmatically.
"""
from document_processor import DocumentProcessor
from chroma_manager import ChromaManager


def main():
    # Configuration
    DOCUMENTS_FOLDER = "./documents"  # Change this to your folder path
    COLLECTION_NAME = "my_documents"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    print("=" * 60)
    print("RAG PIPELINE EXAMPLE")
    print("=" * 60)

    # Step 1: Initialize document processor
    print("\n1. Initializing document processor...")
    processor = DocumentProcessor(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    # Step 2: Process documents
    print(f"\n2. Processing documents from: {DOCUMENTS_FOLDER}")
    try:
        chunks = processor.process_folder(DOCUMENTS_FOLDER)
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease create a 'documents' folder and add some .txt files to it.")
        return

    if not chunks:
        print("No documents found. Please add some .txt files to the documents folder.")
        return

    # Step 3: Initialize ChromaDB
    print("\n3. Initializing ChromaDB...")
    chroma = ChromaManager(collection_name=COLLECTION_NAME)

    # Optional: Reset collection if you want to start fresh
    # chroma.reset_collection()

    # Step 4: Add documents to ChromaDB
    print("\n4. Adding documents to ChromaDB...")
    chroma.add_documents(chunks)

    # Step 5: Display statistics
    print("\n5. Collection statistics:")
    stats = chroma.get_collection_stats()
    print(f"   - Collection: {stats['collection_name']}")
    print(f"   - Total chunks: {stats['total_chunks']}")

    # Step 6: Example queries
    print("\n6. Running example queries...")
    example_queries = [
        "What is the main topic?",
        "Tell me about the key concepts",
    ]

    for query in example_queries:
        print(f"\n   Query: '{query}'")
        results = chroma.query(query, n_results=3)

        if results['documents'][0]:
            print(f"   Found {len(results['documents'][0])} results:")
            for i, doc in enumerate(results['documents'][0]):
                print(f"\n   Result {i + 1}:")
                print(f"   - Source: {results['metadatas'][0][i]['filename']}")
                print(f"   - Distance: {results['distances'][0][i]:.4f}")
                print(f"   - Preview: {doc[:150]}...")
        else:
            print("   No results found.")

    print("\n" + "=" * 60)
    print("EXAMPLE COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Use 'python ingest.py <folder_path>' to ingest your documents")
    print("2. Use 'python query.py' to query interactively")
    print("3. Or integrate this into your own application")


if __name__ == "__main__":
    main()
