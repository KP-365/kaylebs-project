import { useState } from 'react'
import TriageForm from './components/TriageForm'
import ThankYouScreen from './components/ThankYouScreen'
import { TriageResponse } from './types'

function App() {
  const [submitted, setSubmitted] = useState(false)
  const [triageResult, setTriageResult] = useState<TriageResponse | null>(null)

  const handleSubmit = (result: TriageResponse) => {
    setTriageResult(result)
    setSubmitted(true)
  }

  const handleReset = () => {
    setSubmitted(false)
    setTriageResult(null)
  }

  if (submitted) {
    return <ThankYouScreen result={triageResult} onReset={handleReset} />
  }

  return <TriageForm onSubmit={handleSubmit} />
}

export default App


