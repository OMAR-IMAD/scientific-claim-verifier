import { useState } from 'react'
import './App.css'
import { verifyClaim } from './services/api'


function App() {
  const [premise, setPremise] = useState('')
  const [hypothesis, setHypothesis] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleVerify = async () => {
  setError('')
  setResult(null)

  if (!premise.trim() || !hypothesis.trim()) {
    setError('Please enter both premise and hypothesis.')
    return
  }

  setLoading(true)

  try {
    const data = await verifyClaim(premise, hypothesis)
    setResult(data)
  } catch (err) {
    setError(err.message || 'Unable to connect to the backend.')
  } finally {
    setLoading(false)
  }
}

  return (
    <main className="app">
      <section className="hero">
        <p className="eyebrow">NLI-Based Fact-Checking Platform</p>

        <h1>Scientific Claim Verifier</h1>

        <p className="subtitle">
          Analyze a scientific premise and hypothesis to classify their
          relationship as Entailment, Contradiction, or Neutral.
        </p>

        <div className="verification-form">
          <div className="form-group">
            <label htmlFor="premise">Premise</label>

            <textarea
              id="premise"
              value={premise}
              onChange={(event) => setPremise(event.target.value)}
              placeholder="Enter the scientific premise..."
              rows="4"
            />
          </div>

          <div className="form-group">
            <label htmlFor="hypothesis">Hypothesis</label>

            <textarea
              id="hypothesis"
              value={hypothesis}
              onChange={(event) => setHypothesis(event.target.value)}
              placeholder="Enter the hypothesis to verify..."
              rows="4"
            />
          </div>

          <button
            type="button"
            onClick={handleVerify}
            disabled={loading}
          >
            {loading ? 'Verifying...' : 'Verify Claim'}
          </button>

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

          {result && (
            <div className="result-card">
              <h2>{result.prediction}</h2>

              <p>
                Confidence: {(result.confidence * 100).toFixed(2)}%
              </p>

              <p>
                Entailment: {(result.scores.ENTAILMENT * 100).toFixed(2)}%
              </p>

              <p>
                Neutral: {(result.scores.NEUTRAL * 100).toFixed(2)}%
              </p>

              <p>
                Contradiction:{' '}
                {(result.scores.CONTRADICTION * 100).toFixed(2)}%
              </p>
            </div>
          )}
        </div>
      </section>
    </main>
  )
}

export default App