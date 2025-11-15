"""
Script to query documents from ChromaDB.
"""
import argparse
from chroma_manager import ChromaManager


def display_results(results, n_results):
    """Display query results in a readable format."""
    print("\n" + "=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)

    if not results['documents'][0]:
        print("No results found.")
        return

    for i in range(len(results['documents'][0])):
        print(f"\n--- Result {i + 1} ---")
        print(f"Source: {results['metadatas'][0][i]['filename']}")
        print(f"Chunk ID: {results['metadatas'][0][i]['chunk_id']}")
        print(f"Distance: {results['distances'][0][i]:.4f}")
        print(f"\nContent:")
        print(results['documents'][0][i][:300] + "..." if len(results['documents'][0][i]) > 300 else results['documents'][0][i])


def interactive_mode(chroma: ChromaManager, n_results: int):
    """Run interactive query mode."""
    print("\n" + "=" * 60)
    print("INTERACTIVE QUERY MODE")
    print("=" * 60)
    print("Enter your queries (type 'quit' or 'exit' to stop)")

    stats = chroma.get_collection_stats()
    print(f"\nCollection: {stats['collection_name']}")
    print(f"Total chunks: {stats['total_chunks']}")

    while True:
        print("\n" + "-" * 60)
        query = input("\nEnter query: ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("Exiting interactive mode.")
            break

        if not query:
            print("Please enter a valid query.")
            continue

        results = chroma.query(query, n_results=n_results)
        display_results(results, n_results)


def main():
    parser = argparse.ArgumentParser(description='Query documents from ChromaDB')
    parser.add_argument(
        '--query',
        type=str,
        help='Query string (if not provided, enters interactive mode)'
    )
    parser.add_argument(
        '--collection',
        type=str,
        default='documents',
        help='Name of ChromaDB collection (default: documents)'
    )
    parser.add_argument(
        '--n-results',
        type=int,
        default=5,
        help='Number of results to return (default: 5)'
    )

    args = parser.parse_args()

    # Initialize ChromaDB manager
    chroma = ChromaManager(collection_name=args.collection)

    # Check if collection has data
    stats = chroma.get_collection_stats()
    if stats['total_chunks'] == 0:
        print("Collection is empty. Please ingest documents first using ingest.py")
        return

    # Single query mode or interactive mode
    if args.query:
        print(f"\nQuerying: {args.query}")
        results = chroma.query(args.query, n_results=args.n_results)
        display_results(results, args.n_results)
    else:
        interactive_mode(chroma, args.n_results)


if __name__ == "__main__":
    main()
