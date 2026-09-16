from pydantic import ValidationError
from task_1_model_loader import SummaryOutput, ExtractionOutput, ClassificationOutput
MODELS = {"summary": SummaryOutput, "extraction": ExtractionOutput, "classification": ClassificationOutput}

def validate_response(task: str, payload):
    if task not in MODELS:
        return False, "validation_error", "unknown_task"
    try:
        MODELS[task].model_validate(payload)
        return True, None, None
    except ValidationError as exc:
        return False, "validation_error", str(exc)
    except Exception as exc:
        return False, "model_or_runtime_error", str(exc)
