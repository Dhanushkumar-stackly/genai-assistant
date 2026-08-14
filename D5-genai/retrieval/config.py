from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# DIRECTORIES
# ============================================================

DATA_DIR = BASE_DIR / "data"

OUTPUTS_DIR = BASE_DIR / "outputs"

SAMPLES_DIR = BASE_DIR / "samples"


# ============================================================
# INPUT / OUTPUT FILES
# ============================================================

CHUNKS_FILE = OUTPUTS_DIR / "chunks.jsonl"

EMBEDDINGS_FILE = OUTPUTS_DIR / "embeddings.json"

EMBEDDING_METADATA_FILE = OUTPUTS_DIR / "embedding_metadata.json"


# ============================================================
# EMBEDDING CONFIGURATION
# ============================================================

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

EMBEDDING_MODEL = EMBEDDING_MODEL_NAME

EMBEDDING_DIMENSION = 384

BATCH_SIZE = 32


# ============================================================
# CHUNK CONFIGURATION
# ============================================================

CHUNK_SIZE = 500

CHUNK_OVERLAP = 50


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

SAMPLES_DIR.mkdir(parents=True, exist_ok=True)