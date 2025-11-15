# ChromaDB Pipeline

A Python-based Retrieval-Augmented Generation (RAG) pipeline for chunking, storing, and querying unstructured text documents using ChromaDB.

## Features

- Load text documents from a folder
- Intelligent text chunking with overlap
- Vector storage using ChromaDB
- Semantic search capabilities
- Interactive and command-line query modes
- Persistent storage

## Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Prepare Your Documents

Create a folder with your text documents (.txt or .md):

```
documents/
  ├── document1.txt
  ├── document2.txt
  └── document3.md
```

### 2. Ingest Documents

Load and chunk your documents into ChromaDB:

```bash
python ingest.py ./documents
```

With custom options:

```bash
python ingest.py ./documents --collection my_docs --chunk-size 500 --chunk-overlap 100
```

Options:
- `--collection`: Name of the ChromaDB collection (default: documents)
- `--chunk-size`: Size of text chunks in characters (default: 1000)
- `--chunk-overlap`: Overlap between chunks (default: 200)
- `--reset`: Reset the collection before ingesting

### 3. Query Your Documents

**Interactive Mode** (recommended):

```bash
python query.py
```

This starts an interactive session where you can enter multiple queries.

**Single Query Mode**:

```bash
python query.py --query "What is machine learning?"
```

Options:
- `--query`: Query string (if not provided, enters interactive mode)
- `--collection`: Collection to query (default: documents)
- `--n-results`: Number of results to return (default: 5)


**Example Query Output**:

```
------------------------------------------------------------

Enter query: EU

============================================================
SEARCH RESULTS
============================================================

--- Result 1 ---
Source: HOUSE_OVERSIGHT_025215.txt
Chunk ID: 7
Distance: 0.4393

Content:
Europe: Finally (!!), but now what?

--- Result 2 ---
Source: HOUSE_OVERSIGHT_031159.txt
Chunk ID: 7
Distance: 0.4393

Content:
Europe: Finally (!!), but now what?

--- Result 3 ---
Source: HOUSE_OVERSIGHT_030808.txt
Chunk ID: 24
Distance: 0.5147

Content:
Ireland or Spain. Its Italy holdings are less than 2% of the fund, and the portfolio manager does not expect to roll them when they mature.
7 A 2010 Eurobarometer Poll showed very low readings on whether “Membership in the EU is a good thing”. More recently, the centre-left
Foundation for European P...

--- Result 4 ---
Source: HOUSE_OVERSIGHT_011170.txt
Chunk ID: 89
Distance: 0.5162

Content:
should leave the EU https://t.co/EPNk488c9h
https://t.co/3mqaV8v5KD
RT @missingfaktor: Brexit. Grexit. Departugal.
Italeave. Fruckoff. Czechout. Oustria. Finish.
Slovakout. Latervia. Byegium.
Â¿El fin del sueÃ±o europeo? 'Brexit' o 'Bremain', los
britÃ¡nicos deciden suÂ futuro:
Mientras todo el... h...

--- Result 5 ---
Source: HOUSE_OVERSIGHT_011170.txt
Chunk ID: 23
Distance: 0.5180

Content:
23 Jun 2016,
02:37 - CEST
23 Jun 2016,
02:54 - CEST
23 Jun 2016,
02:54 - CEST
23 Jun 2016,
02:54 - CEST
23 Jun 2016,
02:54 - CEST
23 Jun 2016,
02:54 - CEST
23 Jun 2016,
02:54 - CEST
23 Jun 2016,
02:54 - CEST
23 Jun 2016,
02:54 - CEST
23 Jun 2016,
02:54 - CEST
Nantong
City,
Jiangsu,
China
Orlando
, F...

------------------------------------------------------------
```




## Programmatic Usage

Use the modules in your own Python code:

```python
from document_processor import DocumentProcessor
from chroma_manager import ChromaManager

# Process documents
processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
chunks = processor.process_folder("./documents")

# Store in ChromaDB
chroma = ChromaManager(collection_name="my_docs")
chroma.add_documents(chunks)

# Query
results = chroma.query("your question here", n_results=5)
for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
    print(f"Source: {metadata['filename']}")
    print(f"Content: {doc}\n")
```

See `example.py` for a complete example.

## Architecture

### Components

1. **document_processor.py**
   - Loads text documents from a folder
   - Splits documents into chunks using RecursiveCharacterTextSplitter
   - Preserves metadata (source, filename, chunk_id)

2. **chroma_manager.py**
   - Manages ChromaDB operations
   - Handles document storage with embeddings
   - Provides semantic search functionality
   - Persistent storage support

3. **ingest.py**
   - CLI tool for ingesting documents
   - Configurable chunking parameters
   - Collection management

4. **query.py**
   - CLI tool for querying documents
   - Interactive and single-query modes
   - Displays results with metadata

## How It Works

1. **Document Loading**: Text files are loaded from the specified folder
2. **Chunking**: Documents are split into overlapping chunks for better context
3. **Embedding**: ChromaDB automatically generates embeddings using its default embedding model
4. **Storage**: Chunks and embeddings are stored in a persistent ChromaDB collection
5. **Querying**: Semantic search finds the most relevant chunks for your query
6. **Retrieval**: Top-k results are returned with metadata and similarity scores

## Configuration

### Chunk Size

- Larger chunks (1000-2000 chars): Better for preserving context
- Smaller chunks (200-500 chars): More precise matching

### Chunk Overlap

- Recommended: 10-20% of chunk size
- Prevents information loss at chunk boundaries

### Number of Results

- Start with 3-5 results
- Increase if you need more context
- Decrease for more focused answers

## Database Location

ChromaDB persists data to `./chroma_db` by default. This folder contains:
- Vector embeddings
- Document chunks
- Metadata

You can change this in `chroma_manager.py` by modifying the `persist_directory` parameter.

## Integrating with LLMs

To answer questions using an LLM (like OpenAI GPT):

```python
from chroma_manager import ChromaManager
import openai

# Query the database
chroma = ChromaManager()
results = chroma.query("your question", n_results=3)

# Combine results into context
context = "\n\n".join(results['documents'][0])

# Create prompt for LLM
prompt = f"""Answer the question based on the context below.

Context:
{context}

Question: your question

Answer:"""

# Get response from LLM
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)
```

## Troubleshooting

**No results found:**
- Check that documents were ingested successfully
- Try different query phrasings
- Increase `n_results` parameter

**Poor quality results:**
- Adjust chunk size and overlap
- Ensure documents are well-formatted
- Try more specific queries

**Collection is empty:**
- Run `ingest.py` first before querying
- Check that the folder path is correct
- Verify text files are in supported formats

## Next Steps

- Add support for more file formats (PDF, DOCX)
- Implement custom embedding models
- Add metadata filtering
- Create a web interface
- Integrate with LLM APIs for question answering

## License

MIT
