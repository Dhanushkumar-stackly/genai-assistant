import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PROJECT_PATHS = [
    ROOT / "day 1 to 4",
    ROOT / "d5-8 genai assistant",
    ROOT / "d9-d10 genai",
    ROOT / "Genai 11-12",
    ROOT / "Genai_13-14",
    ROOT / "genai-day-15-16",
    ROOT / "genai-day-15-16" / "day15",
    ROOT / "genai-day-15-16" / "day16",
    ROOT / "genai-day-15-16" / "eval",
    ROOT / "genai-day-17-18",
    ROOT / "genai-day-17-18" / "day17",
    ROOT / "genai-day-17-18" / "day18",
]

for path in reversed(PROJECT_PATHS):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)