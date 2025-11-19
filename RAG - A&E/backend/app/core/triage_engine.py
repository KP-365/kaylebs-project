"""
Triage Logic Engine - Rule-based red flag detection
"""
from typing import Dict, List, Optional
from datetime import datetime
from app.models.triage import (
    TriageRequest,
    TriageResponse,
    UrgencyBand,
    RedFlag
)


class TriageEngine:
    """Rule-based triage engine with red flag detection"""
    
    # Red flag rules - deterministic and safe
    RED_FLAG_RULES = {
        "chest_pain": {
            "red": [
                {"condition": lambda a: a.get("shortness_of_breath") == True, 
                 "message": "Chest pain with shortness of breath"},
                {"condition": lambda a: a.get("collapse") == True,
                 "message": "Chest pain with collapse"},
                {"condition": lambda a: a.get("sweating") == True and a.get("nausea") == True,
                 "message": "Chest pain with sweating and nausea"},
                {"condition": lambda a: a.get("heart_disease") == True,
                 "message": "Chest pain with history of heart disease"},
            ],
            "amber": [
                {"condition": lambda a: a.get("age", 0) >= 50,
                 "message": "Chest pain in patient over 50"},
            ]
        },
        "shortness_of_breath": {
            "red": [
                {"condition": lambda a: a.get("chest_pain") == True,
                 "message": "Shortness of breath with chest pain"},
                {"condition": lambda a: a.get("collapse") == True,
                 "message": "Shortness of breath with collapse"},
                {"condition": lambda a: a.get("confusion") == True,
                 "message": "Shortness of breath with confusion"},
                {"condition": lambda a: a.get("severe") == True,
                 "message": "Severe shortness of breath"},
            ],
            "amber": [
                {"condition": lambda a: a.get("wheezing") == True,
                 "message": "Shortness of breath with wheezing"},
            ]
        },
        "abdominal_pain": {
            "red": [
                {"condition": lambda a: a.get("vomiting_blood") == True,
                 "message": "Abdominal pain with vomiting blood"},
                {"condition": lambda a: a.get("severe_bleeding") == True,
                 "message": "Abdominal pain with severe bleeding"},
                {"condition": lambda a: a.get("collapse") == True,
                 "message": "Abdominal pain with collapse"},
                {"condition": lambda a: a.get("pregnant") == True and a.get("severe") == True,
                 "message": "Severe abdominal pain in pregnancy"},
            ],
            "amber": [
                {"condition": lambda a: a.get("fever") == True and a.get("severe") == True,
                 "message": "Severe abdominal pain with fever"},
            ]
        },
        "headache": {
            "red": [
                {"condition": lambda a: a.get("sudden_onset") == True and a.get("severe") == True,
                 "message": "Sudden severe headache"},
                {"condition": lambda a: a.get("confusion") == True,
                 "message": "Headache with confusion"},
                {"condition": lambda a: a.get("vision_loss") == True,
                 "message": "Headache with vision loss"},
                {"condition": lambda a: a.get("neck_stiffness") == True and a.get("fever") == True,
                 "message": "Headache with neck stiffness and fever"},
            ],
            "amber": [
                {"condition": lambda a: a.get("severe") == True,
                 "message": "Severe headache"},
            ]
        },
        "fever_infection": {
            "red": [
                {"condition": lambda a: a.get("confusion") == True,
                 "message": "Fever with confusion"},
                {"condition": lambda a: a.get("severe_bleeding") == True,
                 "message": "Fever with severe bleeding"},
                {"condition": lambda a: a.get("rash") == True and a.get("severe") == True,
                 "message": "Severe fever with rash"},
            ],
            "amber": [
                {"condition": lambda a: a.get("fever_duration", 0) > 3,
                 "message": "Fever lasting more than 3 days"},
            ]
        },
        "injury": {
            "red": [
                {"condition": lambda a: a.get("severe_bleeding") == True,
                 "message": "Injury with severe bleeding"},
                {"condition": lambda a: a.get("loss_of_consciousness") == True,
                 "message": "Injury with loss of consciousness"},
                {"condition": lambda a: a.get("neck_injury") == True,
                 "message": "Neck injury"},
            ],
            "amber": [
                {"condition": lambda a: a.get("unable_to_move_limb") == True,
                 "message": "Injury with inability to move limb"},
            ]
        }
    }
    
    def assess(self, request: TriageRequest) -> TriageResponse:
        """
        Assess patient and return urgency band with red flags
        """
        chief_complaint = request.chief_complaint
        answers = request.answers or {}
        
        # Add age and sex to answers for rule evaluation
        answers["age"] = request.age
        answers["sex"] = request.sex
        
        red_flags: List[RedFlag] = []
        urgency = UrgencyBand.GREEN
        
        # Check red flag rules for the chief complaint
        if chief_complaint in self.RED_FLAG_RULES:
            rules = self.RED_FLAG_RULES[chief_complaint]
            
            # Check red flags first (highest priority)
            for rule in rules.get("red", []):
                try:
                    if rule["condition"](answers):
                        red_flags.append(RedFlag(
                            flag=rule["message"],
                            severity="red"
                        ))
                        urgency = UrgencyBand.RED
                except (KeyError, TypeError):
                    # Skip if required answer not present
                    continue
            
            # Check amber flags (only if no red flags)
            if urgency != UrgencyBand.RED:
                for rule in rules.get("amber", []):
                    try:
                        if rule["condition"](answers):
                            red_flags.append(RedFlag(
                                flag=rule["message"],
                                severity="amber"
                            ))
                            urgency = UrgencyBand.AMBER
                            break  # One amber flag is enough
                    except (KeyError, TypeError):
                        continue
        
        # Generate explanation
        explanation = self._generate_explanation(chief_complaint, red_flags, urgency)
        
        return TriageResponse(
            urgency=urgency,
            red_flags=red_flags,
            explanation=explanation,
            assessed_at=datetime.utcnow(),
            model_version="rule-based-v1.0",
            rule_version="v1.0"
        )
    
    def _generate_explanation(
        self,
        chief_complaint: str,
        red_flags: List[RedFlag],
        urgency: UrgencyBand
    ) -> str:
        """Generate human-readable explanation"""
        complaint_names = {
            "chest_pain": "chest pain",
            "shortness_of_breath": "shortness of breath",
            "abdominal_pain": "abdominal pain",
            "headache": "headache",
            "fever_infection": "fever/infection",
            "injury": "injury"
        }
        
        complaint_name = complaint_names.get(chief_complaint, chief_complaint)
        
        if urgency == UrgencyBand.RED:
            if red_flags:
                flags_text = ", ".join([f.flag for f in red_flags])
                return f"RED: {complaint_name} with red flags: {flags_text}. Requires immediate clinical assessment."
            return f"RED: {complaint_name} requires immediate clinical assessment."
        
        elif urgency == UrgencyBand.AMBER:
            if red_flags:
                flags_text = ", ".join([f.flag for f in red_flags])
                return f"AMBER: {complaint_name} with concerns: {flags_text}. Urgent assessment recommended."
            return f"AMBER: {complaint_name} requires urgent assessment."
        
        else:
            return f"GREEN: {complaint_name} appears low risk. Routine assessment appropriate."


# Singleton instance
triage_engine = TriageEngine()


