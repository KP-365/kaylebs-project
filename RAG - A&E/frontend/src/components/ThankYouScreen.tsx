import { TriageResponse } from '../types'
import './ThankYouScreen.css'

interface ThankYouScreenProps {
  result: TriageResponse | null
  onReset: () => void
}

export default function ThankYouScreen({ result, onReset }: ThankYouScreenProps) {
  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'red':
        return '#f44336'
      case 'amber':
        return '#ff9800'
      case 'green':
        return '#4CAF50'
      default:
        return '#757575'
    }
  }

  const getUrgencyLabel = (urgency: string) => {
    switch (urgency) {
      case 'red':
        return 'RED - Immediate Assessment'
      case 'amber':
        return 'AMBER - Urgent Assessment'
      case 'green':
        return 'GREEN - Routine Assessment'
      default:
        return urgency.toUpperCase()
    }
  }

  return (
    <div className="thank-you-container">
      <div className="thank-you-card">
        <div className="checkmark">✓</div>
        <h1>Thank You</h1>
        <p className="main-message">
          Your assessment has been submitted. A nurse or doctor will review this shortly.
        </p>

        {result && (
          <div className="result-summary">
            <div
              className="urgency-badge"
              style={{ backgroundColor: getUrgencyColor(result.urgency) }}
            >
              {getUrgencyLabel(result.urgency)}
            </div>
            
            {result.red_flags.length > 0 && (
              <div className="red-flags">
                <h3>Key Concerns:</h3>
                <ul>
                  {result.red_flags.map((flag, idx) => (
                    <li key={idx}>{flag.flag}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="explanation">
              <p>{result.explanation}</p>
            </div>

            {/* Debug info - remove in production */}
            <details className="debug-info">
              <summary>Technical Details (for testing)</summary>
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </details>
          </div>
        )}

        <button onClick={onReset} className="big-button secondary">
          Start New Assessment
        </button>
      </div>
    </div>
  )
}


