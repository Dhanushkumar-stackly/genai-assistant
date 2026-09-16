import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/'task-1'/'models.py'
spec=importlib.util.spec_from_file_location('models',p); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
SummaryOutput=mod.SummaryOutput; ExtractionOutput=mod.ExtractionOutput; ClassificationOutput=mod.ClassificationOutput
