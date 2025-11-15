"""
Document processor for loading and chunking text documents.
"""
import os
from pathlib import Path
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentProcessor:
    """Handles loading and chunking of text documents."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor.

        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def load_documents(self, folder_path: str) -> List[Dict[str, str]]:
        """
        Load all text documents from a folder.

        Args:
            folder_path: Path to folder containing text documents

        Returns:
            List of dictionaries with document content and metadata
        """
        documents = []
        folder = Path(folder_path)

        if not folder.exists():
            raise ValueError(f"Folder not found: {folder_path}")

        # Support common text file extensions
        extensions = ['.txt', '.md', '.text', '.doc']

        for file_path in folder.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    documents.append({
                        'content': content,
                        'source': str(file_path),
                        'filename': file_path.name
                    })
                    print(f"Loaded: {file_path.name}")
                except Exception as e:
                    print(f"Error loading {file_path.name}: {e}")

        print(f"\nTotal documents loaded: {len(documents)}")
        return documents

    def chunk_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Split documents into smaller chunks.

        Args:
            documents: List of document dictionaries

        Returns:
            List of chunk dictionaries with content and metadata
        """
        chunks = []

        for doc in documents:
            text_chunks = self.text_splitter.split_text(doc['content'])

            for i, chunk_text in enumerate(text_chunks):
                chunks.append({
                    'content': chunk_text,
                    'source': doc['source'],
                    'filename': doc['filename'],
                    'chunk_id': i
                })

        print(f"Created {len(chunks)} chunks from {len(documents)} documents")
        return chunks

    def process_folder(self, folder_path: str) -> List[Dict[str, str]]:
        """
        Load and chunk all documents in a folder.

        Args:
            folder_path: Path to folder containing text documents

        Returns:
            List of chunk dictionaries
        """
        documents = self.load_documents(folder_path)
        chunks = self.chunk_documents(documents)
        return chunks
