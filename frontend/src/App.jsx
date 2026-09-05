import { useState } from 'react'
import './App.css'

function App() {
  const [premise, setPremise] = useState('')
  const [hypothesis, setHypothesis] = useState('')

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

          <button type="button">
            Verify Claim
          </button>
        </div>
      </section>
    </main>
  )
}

export default App