import { useEffect, useState } from 'react'
import './App.css'
import {
  deleteAnalysis,
  getAnalysisDetail,
  getAnalysisHistory,
  getDashboardStats,
  loginUser,
  verifyClaim,
} from './services/api'

function App() {
  const [premise, setPremise] = useState('')
  const [hypothesis, setHypothesis] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loginLoading, setLoginLoading] = useState(false)
  const [loginMessage, setLoginMessage] = useState('')

  const [isLoggedIn, setIsLoggedIn] = useState(
    Boolean(localStorage.getItem('access_token'))
  )

  const [loggedInEmail, setLoggedInEmail] = useState(
    localStorage.getItem('user_email') || ''
  )

  const [analysisHistory, setAnalysisHistory] = useState([])
  const [historyLoading, setHistoryLoading] = useState(false)
  const [historyError, setHistoryError] = useState('')
  const [historyFilter, setHistoryFilter] = useState('')

  const [selectedAnalysis, setSelectedAnalysis] = useState(null)
    const [detailLoading, setDetailLoading] = useState(false)
    const [detailError, setDetailError] = useState('')

    const [dashboardStats, setDashboardStats] = useState(null)
    const [dashboardLoading, setDashboardLoading] = useState(false)
    const [dashboardError, setDashboardError] = useState('')

  useEffect(() => {
    if (!isLoggedIn) {
      return
    }

    let cancelled = false

    const loadHistory = async () => {
      setHistoryLoading(true)
      setHistoryError('')

      try {
        const data = await getAnalysisHistory(historyFilter)

        if (!cancelled) {
          setAnalysisHistory(Array.isArray(data) ? data : [])
        }
      } catch (err) {
        if (!cancelled) {
          setHistoryError(
            err.message || 'Failed to load analysis history.'
          )
        }
      } finally {
        if (!cancelled) {
          setHistoryLoading(false)
        }
      }
    }

    loadHistory()

    return () => {
      cancelled = true
    }
  }, [isLoggedIn, historyFilter])

useEffect(() => {
  if (!isLoggedIn) {
    return
  }

  let cancelled = false

  const loadDashboardStats = async () => {
    setDashboardLoading(true)
    setDashboardError('')

    try {
      const data = await getDashboardStats()

      if (!cancelled) {
        setDashboardStats(data)
      }
    } catch (err) {
      if (!cancelled) {
        setDashboardError(
          err.message || 'Failed to load dashboard statistics.'
        )
      }
    } finally {
      if (!cancelled) {
        setDashboardLoading(false)
      }
    }
  }

  loadDashboardStats()

  return () => {
    cancelled = true
  }
}, [isLoggedIn])

  const handleViewDetails = async (analysisId) => {
    setDetailLoading(true)
    setDetailError('')
    setSelectedAnalysis(null)

    try {
      const data = await getAnalysisDetail(analysisId)
      setSelectedAnalysis(data)
    } catch (err) {
      setDetailError(
        err.message || 'Failed to load analysis details.'
      )
    } finally {
      setDetailLoading(false)
    }
  }

  const handleCloseDetails = () => {
    setSelectedAnalysis(null)
    setDetailError('')
  }

  const handleDeleteAnalysis = async (analysisId) => {
    const confirmed = window.confirm(
      'Are you sure you want to delete this analysis?'
    )

    if (!confirmed) {
      return
    }

    setHistoryError('')

    try {
      await deleteAnalysis(analysisId)

      setAnalysisHistory((currentHistory) =>
        currentHistory.filter(
          (analysis) => analysis.id !== analysisId
        )
      )

      if (selectedAnalysis?.id === analysisId) {
        setSelectedAnalysis(null)
      }
    } catch (err) {
      setHistoryError(
        err.message || 'Failed to delete analysis.'
      )
    }
  }

  const handleLogin = async () => {
    setLoginMessage('')

    if (!email.trim() || !password) {
      setLoginMessage('Please enter email and password.')
      return
    }

    setLoginLoading(true)

    try {
      const userEmail = email.trim()

      await loginUser(userEmail, password)

      localStorage.setItem('user_email', userEmail)
      setLoggedInEmail(userEmail)
      setIsLoggedIn(true)

      setLoginMessage('Login successful.')
      setPassword('')
    } catch (err) {
      setLoginMessage(err.message || 'Login failed.')
    } finally {
      setLoginLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_email')

    setIsLoggedIn(false)
    setLoggedInEmail('')

    setLoginMessage('Logged out successfully.')
    setEmail('')
    setPassword('')

    setResult(null)
    setError('')

    setAnalysisHistory([])
    setHistoryError('')
    setHistoryFilter('')

    setSelectedAnalysis(null)
    setDetailError('')
    setDetailLoading(false)
  }

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

      try {
        const historyData = await getAnalysisHistory(historyFilter)

        setAnalysisHistory(
          Array.isArray(historyData) ? historyData : []
        )
      } catch (historyErr) {
        setHistoryError(
          historyErr.message ||
            'Failed to refresh analysis history.'
        )
      }

      try {
        setDashboardError('')

        const statsData = await getDashboardStats()
        setDashboardStats(statsData)
      } catch (dashboardErr) {
        setDashboardError(
          dashboardErr.message ||
            'Failed to refresh dashboard statistics.'
        )
      }
      try {
        setDashboardError('')

        const statsData = await getDashboardStats()
        setDashboardStats(statsData)
      } catch (dashboardErr) {
        setDashboardError(
          dashboardErr.message ||
            'Failed to refresh dashboard statistics.'
        )
      }

    } catch (err) {
      setError(
        err.message || 'Unable to connect to the backend.'
      )
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setPremise('')
    setHypothesis('')
    setResult(null)
    setError('')
  }

  const handleRefreshHistory = async () => {
    setHistoryLoading(true)
    setHistoryError('')

    try {
      const data = await getAnalysisHistory(historyFilter)

      setAnalysisHistory(
        Array.isArray(data) ? data : []
      )
    } catch (err) {
      setHistoryError(
        err.message || 'Failed to load analysis history.'
      )
    } finally {
      setHistoryLoading(false)
    }
  }

  return (
    <main className="app">
      <section className="hero">
        <p className="eyebrow">
          NLI-Based Fact-Checking Platform
        </p>

        <h1>Scientific Claim Verifier</h1>

        <p className="subtitle">
          Analyze a scientific premise and hypothesis to classify
          their relationship as Entailment, Contradiction, or Neutral.
        </p>

        {!isLoggedIn ? (
          <div className="login-form">
            <div className="form-group">
              <label htmlFor="email">Email</label>

              <input
                id="email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="Enter your email..."
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>

              <input
                id="password"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="Enter your password..."
              />
            </div>

            <button
              type="button"
              onClick={handleLogin}
              disabled={loginLoading}
            >
              {loginLoading ? 'Logging in...' : 'Login'}
            </button>

            {loginMessage && (
              <p className="login-message">
                {loginMessage}
              </p>
            )}
          </div>
        ) : (
          <div className="login-form">
            <p className="login-message">
              Logged in as: {loggedInEmail}
            </p>

            <button
              type="button"
              onClick={handleLogout}
            >
              Logout
            </button>
          </div>
        )}

        {isLoggedIn && (
          <>
<div className="dashboard-section">
  <h2>Dashboard</h2>

  {dashboardLoading && (
    <p className="login-message">
      Loading dashboard statistics...
    </p>
  )}

  {dashboardError && (
    <p className="error-message">
      {dashboardError}
    </p>
  )}

  {dashboardStats && (
    <div className="dashboard-cards">
      <div className="dashboard-card">
        <span>Total Analyses</span>
        <strong>{dashboardStats.total}</strong>
      </div>

      <div className="dashboard-card">
        <span>Entailment</span>
        <strong>{dashboardStats.ENTAILMENT}</strong>
        <small>
          {dashboardStats.entailment_percentage.toFixed(2)}%
        </small>
      </div>

      <div className="dashboard-card">
        <span>Neutral</span>
        <strong>{dashboardStats.NEUTRAL}</strong>
        <small>
          {dashboardStats.neutral_percentage.toFixed(2)}%
        </small>
      </div>

      <div className="dashboard-card">
        <span>Contradiction</span>
        <strong>{dashboardStats.CONTRADICTION}</strong>
        <small>
          {dashboardStats.contradiction_percentage.toFixed(2)}%
        </small>
      </div>
    </div>
  )}
</div>
            <div className="verification-form">
              <div className="form-group">
                <label htmlFor="premise">
                  Premise
                </label>

                <textarea
                  id="premise"
                  value={premise}
                  onChange={(event) =>
                    setPremise(event.target.value)
                  }
                  placeholder="Enter the scientific premise..."
                  rows="4"
                />
              </div>

              <div className="form-group">
                <label htmlFor="hypothesis">
                  Hypothesis
                </label>

                <textarea
                  id="hypothesis"
                  value={hypothesis}
                  onChange={(event) =>
                    setHypothesis(event.target.value)
                  }
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

              <button
                type="button"
                onClick={handleClear}
                disabled={loading}
              >
                Clear Form
              </button>

              {error && (
                <p className="error-message">
                  {error}
                </p>
              )}

              {result && (
                <div className="result-card">
                  <div className="result-header">
                    <p className="result-title">
                      Prediction
                    </p>

                    <h2>{result.prediction}</h2>

                    <p className="confidence-value">
                      Confidence:{' '}
                      {(result.confidence * 100).toFixed(2)}%
                    </p>
                  </div>

                  <div className="score-list">
                    <div className="score-item">
                      <div className="score-row">
                        <span>Entailment</span>

                        <strong>
                          {(
                            result.scores.ENTAILMENT * 100
                          ).toFixed(2)}
                          %
                        </strong>
                      </div>

                      <div className="score-bar">
                        <div
                          className="score-fill entailment"
                          style={{
                            width: `${
                              result.scores.ENTAILMENT * 100
                            }%`,
                          }}
                        />
                      </div>
                    </div>

                    <div className="score-item">
                      <div className="score-row">
                        <span>Neutral</span>

                        <strong>
                          {(
                            result.scores.NEUTRAL * 100
                          ).toFixed(2)}
                          %
                        </strong>
                      </div>

                      <div className="score-bar">
                        <div
                          className="score-fill neutral"
                          style={{
                            width: `${
                              result.scores.NEUTRAL * 100
                            }%`,
                          }}
                        />
                      </div>
                    </div>

                    <div className="score-item">
                      <div className="score-row">
                        <span>Contradiction</span>

                        <strong>
                          {(
                            result.scores.CONTRADICTION * 100
                          ).toFixed(2)}
                          %
                        </strong>
                      </div>

                      <div className="score-bar">
                        <div
                          className="score-fill contradiction"
                          style={{
                            width: `${
                              result.scores.CONTRADICTION * 100
                            }%`,
                          }}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="history-section">
              <div className="history-header">
                <h2>Analysis History</h2>

                <button
                  type="button"
                  onClick={handleRefreshHistory}
                  disabled={historyLoading}
                >
                  {historyLoading
                    ? 'Loading...'
                    : 'Refresh History'}
                </button>
              </div>

              <div className="history-filters">
                <button
                  type="button"
                  className={
                    historyFilter === '' ? 'active' : ''
                  }
                  onClick={() => setHistoryFilter('')}
                  disabled={historyLoading}
                >
                  All
                </button>

                <button
                  type="button"
                  className={
                    historyFilter === 'ENTAILMENT'
                      ? 'active'
                      : ''
                  }
                  onClick={() =>
                    setHistoryFilter('ENTAILMENT')
                  }
                  disabled={historyLoading}
                >
                  Entailment
                </button>

                <button
                  type="button"
                  className={
                    historyFilter === 'NEUTRAL'
                      ? 'active'
                      : ''
                  }
                  onClick={() =>
                    setHistoryFilter('NEUTRAL')
                  }
                  disabled={historyLoading}
                >
                  Neutral
                </button>

                <button
                  type="button"
                  className={
                    historyFilter === 'CONTRADICTION'
                      ? 'active'
                      : ''
                  }
                  onClick={() =>
                    setHistoryFilter('CONTRADICTION')
                  }
                  disabled={historyLoading}
                >
                  Contradiction
                </button>
              </div>

              {historyError && (
                <p className="error-message">
                  {historyError}
                </p>
              )}

              {detailLoading && (
                <p className="login-message">
                  Loading analysis details...
                </p>
              )}

              {detailError && (
                <p className="error-message">
                  {detailError}
                </p>
              )}

              {selectedAnalysis && (
                <div className="result-card">
                  <div className="result-header">
                    <p className="result-title">
                      Analysis Details
                    </p>

                    <h2>
                      {selectedAnalysis.prediction}
                    </h2>

                    <p className="confidence-value">
                      Confidence:{' '}
                      {(
                        selectedAnalysis.confidence * 100
                      ).toFixed(2)}
                      %
                    </p>
                  </div>

                  <div className="score-list">
                    <p>
                      <strong>Premise:</strong>{' '}
                      {selectedAnalysis.premise}
                    </p>

                    <p>
                      <strong>Hypothesis:</strong>{' '}
                      {selectedAnalysis.hypothesis}
                    </p>

                    <p>
                      <strong>Entailment:</strong>{' '}
                      {(
                        selectedAnalysis.entailment_score *
                        100
                      ).toFixed(2)}
                      %
                    </p>

                    <p>
                      <strong>Neutral:</strong>{' '}
                      {(
                        selectedAnalysis.neutral_score * 100
                      ).toFixed(2)}
                      %
                    </p>

                    <p>
                      <strong>Contradiction:</strong>{' '}
                      {(
                        selectedAnalysis.contradiction_score *
                        100
                      ).toFixed(2)}
                      %
                    </p>

                    <p className="history-date">
                      {new Date(
                        selectedAnalysis.created_at
                      ).toLocaleString()}
                    </p>

                    <button
                      type="button"
                      onClick={handleCloseDetails}
                    >
                      Close Details
                    </button>
                  </div>
                </div>
              )}

              {!historyLoading &&
                !historyError &&
                analysisHistory.length === 0 && (
                  <p className="history-empty">
                    No analyses found for this filter.
                  </p>
                )}

              <div className="history-list">
                {analysisHistory.map((analysis) => (
                  <div
                    className="history-card"
                    key={analysis.id}
                  >
                    <div className="history-card-header">
                      <strong>
                        {analysis.prediction}
                      </strong>

                      <span>
                        {(
                          analysis.confidence * 100
                        ).toFixed(2)}
                        %
                      </span>
                    </div>

                    <p>
                      <strong>Premise:</strong>{' '}
                      {analysis.premise}
                    </p>

                    <p>
                      <strong>Hypothesis:</strong>{' '}
                      {analysis.hypothesis}
                    </p>

                    <p>
                      Entailment:{' '}
                      {(
                        analysis.entailment_score * 100
                      ).toFixed(2)}
                      %
                    </p>

                    <p>
                      Neutral:{' '}
                      {(
                        analysis.neutral_score * 100
                      ).toFixed(2)}
                      %
                    </p>

                    <p>
                      Contradiction:{' '}
                      {(
                        analysis.contradiction_score * 100
                      ).toFixed(2)}
                      %
                    </p>

                    <p className="history-date">
                      {new Date(
                        analysis.created_at
                      ).toLocaleString()}
                    </p>

                    <button
                      type="button"
                      onClick={() =>
                        handleViewDetails(analysis.id)
                      }
                      disabled={detailLoading}
                    >
                      View Details
                    </button>

                    <button
                      type="button"
                      onClick={() =>
                        handleDeleteAnalysis(analysis.id)
                      }
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </section>
    </main>
  )
}

export default App