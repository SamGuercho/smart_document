"""
Default configuration settings for the model package.
"""

DEFAULT_CONFIG = {
    "classifier": {
        "type": "llm",  # "llm" or "ml"
        "model_name": "gpt-4",
        "confidence_threshold": 0.7,
        "batch_size": 10
    },
    "extractor": {
        "type": "llm",  # "llm" or "rule"
        "model_name": "gpt-4",
        "extract_fields": [
            "document_date",
            "total_amount", 
            "currency",
            "parties"
        ],
        "confidence_threshold": 0.6
    },
    "pipeline": {
        "enable_validation": True,
        "save_intermediate_results": False,
        "max_retries": 3,
        "timeout": 30
    },
    "processing": {
        "max_file_size_mb": 50,
        "supported_formats": [".pdf"],
        "temp_dir": "./temp",
        "output_dir": "./output"
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "model.log"
    }
} 