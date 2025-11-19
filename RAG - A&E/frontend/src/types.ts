export interface TriageRequest {
  age: number
  sex: 'M' | 'F' | 'Other'
  chief_complaint: string
  answers: Record<string, any>
  patient_id?: string
}

export interface RedFlag {
  flag: string
  severity: string
}

export interface TriageResponse {
  urgency: 'red' | 'amber' | 'green'
  red_flags: RedFlag[]
  explanation: string
  assessed_at: string
  model_version: string
  rule_version: string
}


