import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHROMA_DIR = PROJECT_ROOT / "outputs" / "chroma_db"

COLLECTION_NAME = "genai_documents"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

def load_embedding_model():

    print("Loading embedding model...")

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    print(
        f"Model loaded: {EMBEDDING_MODEL}"
    )

    return model


# ============================================================
# LOAD VECTOR DATABASE
# ============================================================

def load_collection():

    print("Loading vector database...")

    print(
        f"ChromaDB path: {CHROMA_DIR}"
    )

    # --------------------------------------------------------
    # Check database directory
    # --------------------------------------------------------

    if not CHROMA_DIR.exists():

        raise FileNotFoundError(
            f"ChromaDB directory not found:\n"
            f"{CHROMA_DIR}\n\n"
            f"Run build_vector_index.py first."
        )

    # --------------------------------------------------------
    # Create persistent ChromaDB client
    # --------------------------------------------------------

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    # --------------------------------------------------------
    # Display available collections
    # --------------------------------------------------------

    collections = client.list_collections()

    print("Available collections:")

    if not collections:

        print("  No collections found.")

    else:

        for collection in collections:

            print(
                f"  - {collection.name}"
            )

    # --------------------------------------------------------
    # Get required collection
    # --------------------------------------------------------

    try:

        collection = client.get_collection(
            name=COLLECTION_NAME
        )

    except Exception as e:

        raise RuntimeError(
            f"\nCollection '{COLLECTION_NAME}' "
            f"does not exist.\n\n"
            f"Run:\n"
            f"python scripts/build_vector_index.py"
        ) from e

    print(
        f"Collection loaded: {COLLECTION_NAME}"
    )

    print(
        f"Total vectors: {collection.count()}"
    )

    return collection


# ============================================================
# RETRIEVE RELEVANT DOCUMENTS
# ============================================================

def retrieve(
    question,
    top_k=5
):

    print("\n" + "=" * 60)
    print("RETRIEVAL")
    print("=" * 60)

    print(
        f"Question: {question}"
    )

    # --------------------------------------------------------
    # STEP 1: Load embedding model
    # --------------------------------------------------------

    model = load_embedding_model()

    # --------------------------------------------------------
    # STEP 2: Load vector database
    # --------------------------------------------------------

    collection = load_collection()

    # --------------------------------------------------------
    # STEP 3: Convert question to embedding
    # --------------------------------------------------------

    print(
        "Generating query embedding..."
    )

    query_embedding = model.encode(
        question,
        convert_to_numpy=True
    )

    print(
        f"Query embedding dimension: "
        f"{len(query_embedding)}"
    )

    # --------------------------------------------------------
    # STEP 4: Similarity search
    # --------------------------------------------------------

    print(
        f"Searching top {top_k} relevant chunks..."
    )

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    # --------------------------------------------------------
    # STEP 5: Extract results
    # --------------------------------------------------------

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    # --------------------------------------------------------
    # STEP 6: Prepare final results
    # --------------------------------------------------------

    retrieved_results = []

    for i in range(len(documents)):

        # Get metadata safely
        metadata = metadatas[i]

        if not isinstance(metadata, dict):

            metadata = {}

        # Get chunk ID
        chunk_id = metadata.get(
            "chunk_id",
            f"chunk_{i:04d}"
        )

        # Create result
        result = {

            "rank": i + 1,

            "chunk_id": str(
                chunk_id
            ),

            "text": documents[i],

            "metadata": metadata,

            "distance": distances[i]
        }

        retrieved_results.append(
            result
        )

    # --------------------------------------------------------
    # STEP 7: Display retrieved chunks
    # --------------------------------------------------------

    print("\nRetrieved chunks:")

    print("-" * 60)

    for result in retrieved_results:

        print(
            f"\nRank: {result['rank']}"
        )

        print(
            f"Chunk ID: {result['chunk_id']}"
        )

        print(
            f"Distance: {result['distance']}"
        )

        print(
            f"Metadata: {result['metadata']}"
        )

        print(
            f"Text: {result['text'][:500]}"
        )

        print("-" * 60)

    # --------------------------------------------------------
    # STEP 8: Return results
    # --------------------------------------------------------

    return retrieved_results


# ============================================================
# MAIN / TEST
# ============================================================

if __name__ == "__main__":

    question = (
        "What are the responsibilities "
        "of the team members?"
    )

    results = retrieve(
        question,
        top_k=5
    )

    print("\n" + "=" * 60)
    print("RETRIEVAL SUMMARY")
    print("=" * 60)

    print(
        f"Question: {question}"
    )

    print(
        f"Results returned: {len(results)}"
    )

    for result in results:

        print(
            f"{result['rank']}. "
            f"{result['chunk_id']} "
            f"| distance="
            f"{result['distance']}"
        )