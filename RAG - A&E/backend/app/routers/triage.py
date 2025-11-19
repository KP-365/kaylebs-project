"""
Triage router - handles triage assessment requests
"""
from fastapi import APIRouter, HTTPException
from app.models.triage import TriageRequest, TriageResponse
from app.core.triage_engine import triage_engine
from app.core.logging import log_triage_request

router = APIRouter()


@router.post("/triage", response_model=TriageResponse)
async def assess_triage(request: TriageRequest) -> TriageResponse:
    """
    Assess patient triage and return urgency band with red flags
    
    Accepts patient information and symptom answers, returns:
    - Urgency band (red/amber/green)
    - List of red flags detected
    - Human-readable explanation
    """
    try:
        # Validate chief complaint
        valid_complaints = [
            "chest_pain",
            "shortness_of_breath",
            "abdominal_pain",
            "headache",
            "fever_infection",
            "injury"
        ]
        
        if request.chief_complaint not in valid_complaints:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid chief complaint. Must be one of: {', '.join(valid_complaints)}"
            )
        
        # Perform triage assessment
        response = triage_engine.assess(request)
        
        # Log the request and response
        log_triage_request(request, response)
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        # Safety fallback: if anything fails, mark as higher urgency
        log_triage_request(request, None, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Unable to assess. Please see clinician immediately."
        )


