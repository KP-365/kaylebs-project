import { useState } from 'react'
import axios from 'axios'
import { TriageRequest, TriageResponse } from '../types'
import './TriageForm.css'

const CHIEF_COMPLAINTS = [
  { value: 'chest_pain', label: 'Chest Pain' },
  { value: 'shortness_of_breath', label: 'Shortness of Breath' },
  { value: 'abdominal_pain', label: 'Abdominal Pain' },
  { value: 'headache', label: 'Headache' },
  { value: 'fever_infection', label: 'Fever/Infection' },
  { value: 'injury', label: 'Injury' },
]

interface TriageFormProps {
  onSubmit: (result: TriageResponse) => void
}

export default function TriageForm({ onSubmit }: TriageFormProps) {
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const [formData, setFormData] = useState<Partial<TriageRequest>>({
    age: undefined,
    sex: undefined,
    chief_complaint: undefined,
    answers: {},
  })

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleAnswerChange = (key: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      answers: {
        ...prev.answers,
        [key]: value,
      },
    }))
  }

  const handleNext = () => {
    if (step === 1 && formData.age && formData.sex) {
      setStep(2)
    } else if (step === 2 && formData.chief_complaint) {
      setStep(3)
    }
  }

  const handleBack = () => {
    setStep(prev => Math.max(1, prev - 1))
  }

  const handleSubmit = async () => {
    if (!formData.age || !formData.sex || !formData.chief_complaint) {
      setError('Please complete all required fields')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const request: TriageRequest = {
        age: formData.age!,
        sex: formData.sex as 'M' | 'F' | 'Other',
        chief_complaint: formData.chief_complaint!,
        answers: formData.answers || {},
      }

      const response = await axios.post<TriageResponse>(
        '/api/triage',
        request
      )

      onSubmit(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const renderStep1 = () => (
    <div className="step">
      <h2>Basic Information</h2>
      <div className="form-group">
        <label>Age (must be 18 or older)</label>
        <input
          type="number"
          min="18"
          max="120"
          value={formData.age || ''}
          onChange={(e) => handleInputChange('age', parseInt(e.target.value))}
          className="big-input"
        />
      </div>
      <div className="form-group">
        <label>Sex</label>
        <div className="button-group">
          <button
            type="button"
            className={`big-button ${formData.sex === 'M' ? 'active' : ''}`}
            onClick={() => handleInputChange('sex', 'M')}
          >
            Male
          </button>
          <button
            type="button"
            className={`big-button ${formData.sex === 'F' ? 'active' : ''}`}
            onClick={() => handleInputChange('sex', 'F')}
          >
            Female
          </button>
          <button
            type="button"
            className={`big-button ${formData.sex === 'Other' ? 'active' : ''}`}
            onClick={() => handleInputChange('sex', 'Other')}
          >
            Other
          </button>
        </div>
      </div>
    </div>
  )

  const renderStep2 = () => (
    <div className="step">
      <h2>What is your main problem?</h2>
      <div className="button-group vertical">
        {CHIEF_COMPLAINTS.map(complaint => (
          <button
            key={complaint.value}
            type="button"
            className={`big-button ${formData.chief_complaint === complaint.value ? 'active' : ''}`}
            onClick={() => handleInputChange('chief_complaint', complaint.value)}
          >
            {complaint.label}
          </button>
        ))}
      </div>
    </div>
  )

  const renderStep3 = () => {
    const complaint = formData.chief_complaint
    
    const getQuestions = () => {
      switch (complaint) {
        case 'chest_pain':
          return [
            { key: 'shortness_of_breath', label: 'Are you short of breath?', type: 'yesno' },
            { key: 'sweating', label: 'Are you sweating?', type: 'yesno' },
            { key: 'nausea', label: 'Do you feel nauseous?', type: 'yesno' },
            { key: 'collapse', label: 'Did you collapse or feel like collapsing?', type: 'yesno' },
            { key: 'heart_disease', label: 'Do you have a history of heart disease?', type: 'yesno' },
          ]
        case 'shortness_of_breath':
          return [
            { key: 'chest_pain', label: 'Do you have chest pain?', type: 'yesno' },
            { key: 'collapse', label: 'Did you collapse?', type: 'yesno' },
            { key: 'confusion', label: 'Are you confused?', type: 'yesno' },
            { key: 'severe', label: 'Is it severe?', type: 'yesno' },
            { key: 'wheezing', label: 'Do you have wheezing?', type: 'yesno' },
          ]
        case 'abdominal_pain':
          return [
            { key: 'vomiting_blood', label: 'Are you vomiting blood?', type: 'yesno' },
            { key: 'severe_bleeding', label: 'Are you bleeding severely?', type: 'yesno' },
            { key: 'collapse', label: 'Did you collapse?', type: 'yesno' },
            { key: 'pregnant', label: 'Are you pregnant?', type: 'yesno' },
            { key: 'severe', label: 'Is the pain severe?', type: 'yesno' },
            { key: 'fever', label: 'Do you have a fever?', type: 'yesno' },
          ]
        case 'headache':
          return [
            { key: 'sudden_onset', label: 'Did it start suddenly?', type: 'yesno' },
            { key: 'severe', label: 'Is it severe?', type: 'yesno' },
            { key: 'confusion', label: 'Are you confused?', type: 'yesno' },
            { key: 'vision_loss', label: 'Have you lost vision?', type: 'yesno' },
            { key: 'neck_stiffness', label: 'Do you have neck stiffness?', type: 'yesno' },
            { key: 'fever', label: 'Do you have a fever?', type: 'yesno' },
          ]
        case 'fever_infection':
          return [
            { key: 'confusion', label: 'Are you confused?', type: 'yesno' },
            { key: 'severe_bleeding', label: 'Are you bleeding severely?', type: 'yesno' },
            { key: 'rash', label: 'Do you have a rash?', type: 'yesno' },
            { key: 'severe', label: 'Is it severe?', type: 'yesno' },
            { key: 'fever_duration', label: 'How many days has the fever lasted?', type: 'number' },
          ]
        case 'injury':
          return [
            { key: 'severe_bleeding', label: 'Are you bleeding severely?', type: 'yesno' },
            { key: 'loss_of_consciousness', label: 'Did you lose consciousness?', type: 'yesno' },
            { key: 'neck_injury', label: 'Is it a neck injury?', type: 'yesno' },
            { key: 'unable_to_move_limb', label: 'Are you unable to move a limb?', type: 'yesno' },
          ]
        default:
          return []
      }
    }

    const questions = getQuestions()

    return (
      <div className="step">
        <h2>Please answer these questions</h2>
        {questions.map(q => (
          <div key={q.key} className="form-group">
            <label>{q.label}</label>
            {q.type === 'yesno' ? (
              <div className="button-group">
                <button
                  type="button"
                  className={`big-button ${formData.answers?.[q.key] === true ? 'active' : ''}`}
                  onClick={() => handleAnswerChange(q.key, true)}
                >
                  Yes
                </button>
                <button
                  type="button"
                  className={`big-button ${formData.answers?.[q.key] === false ? 'active' : ''}`}
                  onClick={() => handleAnswerChange(q.key, false)}
                >
                  No
                </button>
              </div>
            ) : (
              <input
                type="number"
                min="0"
                value={formData.answers?.[q.key] || ''}
                onChange={(e) => handleAnswerChange(q.key, parseInt(e.target.value))}
                className="big-input"
              />
            )}
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="triage-form-container">
      <div className="triage-form">
        <h1>AI Triage Assessment</h1>
        
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${(step / 3) * 100}%` }} />
        </div>

        {error && <div className="error-message">{error}</div>}

        {step === 1 && renderStep1()}
        {step === 2 && renderStep2()}
        {step === 3 && renderStep3()}

        <div className="form-actions">
          {step > 1 && (
            <button type="button" onClick={handleBack} className="big-button secondary">
              Back
            </button>
          )}
          {step < 3 ? (
            <button
              type="button"
              onClick={handleNext}
              className="big-button primary"
              disabled={
                (step === 1 && (!formData.age || !formData.sex)) ||
                (step === 2 && !formData.chief_complaint)
              }
            >
              Next
            </button>
          ) : (
            <button
              type="button"
              onClick={handleSubmit}
              className="big-button primary"
              disabled={loading}
            >
              {loading ? 'Submitting...' : 'Submit'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}


