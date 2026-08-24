from dataclasses import asdict, dataclass
from typing import Any


# ============================================================
# DAY-09 BASELINE CONFIGURATION
# ============================================================

@dataclass(frozen=True)
class BaselineConfig:
    """
    Configuration that will be frozen for Day-09 experiments.
    """

    embedding_model: str
    chunk_size: int
    chunk_overlap: int
    top_k: int
    metadata_filters: dict[str, Any]
    score_threshold: float
    prompt_version: str

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the configuration object into a dictionary.
        """

        return asdict(self)


# ============================================================
# FROZEN BASELINE
# ============================================================

BASELINE_CONFIG = BaselineConfig(
    embedding_model="YOUR_EMBEDDING_MODEL",
    chunk_size=500,
    chunk_overlap=50,
    top_k=5,
    metadata_filters={},
    score_threshold=0.70,
    prompt_version="v1",
)