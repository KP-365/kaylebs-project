"""
Logging utilities
"""
import logging
import json
from datetime import datetime
from typing import Optional
from app.models.triage import TriageRequest, TriageResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('triage.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_triage_request(
    request: TriageRequest,
    response: Optional[TriageResponse],
    error: Optional[str] = None
):
    """Log triage request and response"""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "patient_id": request.patient_id,
        "age": request.age,
        "sex": request.sex,
        "chief_complaint": request.chief_complaint,
        "answers": request.answers,
    }
    
    if error:
        log_entry["error"] = error
        log_entry["status"] = "error"
        logger.error(f"Triage error: {json.dumps(log_entry)}")
    else:
        log_entry["urgency"] = response.urgency.value
        log_entry["red_flags"] = [f.flag for f in response.red_flags]
        log_entry["model_version"] = response.model_version
        log_entry["rule_version"] = response.rule_version
        log_entry["status"] = "success"
        logger.info(f"Triage assessment: {json.dumps(log_entry)}")


