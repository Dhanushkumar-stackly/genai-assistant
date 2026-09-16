from pathlib import Path
PROMPT_PATH = Path(__file__).with_name("extraction.txt")
def build_extraction_prompt(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Source text must be non-empty.")
    return f"{PROMPT_PATH.read_text(encoding='utf-8').strip()}\n\nSOURCE TEXT:\n{text.strip()}"
