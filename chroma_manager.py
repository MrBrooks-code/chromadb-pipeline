"""
ChromaDB manager for storing and querying document chunks.
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict
import uuid


class ChromaManager:
    """Manages ChromaDB operations for document storage and retrieval."""

    def __init__(self, collection_name: str = "documents", persist_directory: str = "./chroma_db"):
        """
        Initialize ChromaDB client and collection.

        Args:
            collection_name: Name of the collection to use
            persist_directory: Directory to persist the database
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )

        print(f"ChromaDB initialized with collection: {collection_name}")
        print(f"Persist directory: {persist_directory}")

    def add_documents(self, chunks: List[Dict[str, str]]):
        """
        Add document chunks to ChromaDB.

        Args:
            chunks: List of chunk dictionaries with content and metadata
        """
        if not chunks:
            print("No chunks to add")
            return

        documents = []
        metadatas = []
        ids = []

        for chunk in chunks:
            # Generate unique ID for each chunk
            chunk_id = str(uuid.uuid4())

            documents.append(chunk['content'])
            metadatas.append({
                'source': chunk['source'],
                'filename': chunk['filename'],
                'chunk_id': str(chunk['chunk_id'])
            })
            ids.append(chunk_id)

        # Add to collection in batches to avoid memory issues
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_metas = metadatas[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]

            self.collection.add(
                documents=batch_docs,
                metadatas=batch_metas,
                ids=batch_ids
            )

        print(f"Added {len(documents)} chunks to ChromaDB")

    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """
        Query the collection for similar documents.

        Args:
            query_text: Query string
            n_results: Number of results to return

        Returns:
            Dictionary containing results with documents, metadatas, and distances
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

        return results

    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the current collection.

        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        return {
            'collection_name': self.collection_name,
            'total_chunks': count,
            'persist_directory': self.persist_directory
        }

    def delete_collection(self):
        """Delete the current collection."""
        self.client.delete_collection(name=self.collection_name)
        print(f"Deleted collection: {self.collection_name}")

    def reset_collection(self):
        """Reset the collection by deleting and recreating it."""
        self.delete_collection()
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"Reset collection: {self.collection_name}")
