import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Defined expected schema
REQUIRED_FIELDS = {
    "study_id": str,
    "study_name": str,
    "pi_name": str,
    "pi_email": str,
    "lab_email": str,
}

def validate_study_info(json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Study info file not found: {json_path}")

    with open(json_path, "r") as f:
        try:
            info = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {json_path}: {e}")
    
    # Validate keys and types:
    for key, expected_type in REQUIRED_FIELDS.items():
        if key not in info:
            raise ValueError(f"Missing required field '{key}' in {json_path}")
        if not isinstance(info[key], expected_type):
            raise TypeError(f"Field '{key} in {json_path} should be of type {expected_type.__name__}")

    print(f"✓ Validated: {os.path.basename(json_path)}")
    return info