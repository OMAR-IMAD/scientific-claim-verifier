const API_BASE_URL = 'http://127.0.0.1:8000'

export async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email.trim(),
      password,
    }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || 'Login failed.')
  }

  localStorage.setItem('access_token', data.access_token)

  return data
}

export async function registerUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email.trim(),
      password,
    }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(
      typeof data.detail === 'string'
        ? data.detail
        : 'Registration failed.'
    )
  }

  return data
}

export async function verifyClaim(premise, hypothesis) {
  const token = localStorage.getItem('access_token')

  if (!token) {
    throw new Error('No access token found. Please log in first.')
  }

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      premise: premise.trim(),
      hypothesis: hypothesis.trim(),
    }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || 'Prediction request failed.')
  }

  return data
}

export async function getAnalysisHistory(prediction = '') {
  const token = localStorage.getItem('access_token')

  if (!token) {
    throw new Error('No access token found. Please log in first.')
  }

  const params = new URLSearchParams()

  if (prediction) {
    params.set('prediction', prediction)
  }

  const queryString = params.toString()

  const url = queryString
    ? `${API_BASE_URL}/history?${queryString}`
    : `${API_BASE_URL}/history`

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(
      data.detail || 'Failed to load analysis history.'
    )
  }

  return data
}

export async function getAnalysisDetail(analysisId) {
  const token = localStorage.getItem('access_token')

  if (!token) {
    throw new Error('No access token found. Please log in first.')
  }

  const response = await fetch(
    `${API_BASE_URL}/history/${analysisId}`,
    {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )

  const data = await response.json()

  if (!response.ok) {
    throw new Error(
      data.detail || 'Failed to load analysis details.'
    )
  }

  return data
}

export async function deleteAnalysis(analysisId) {
  const token = localStorage.getItem('access_token')

  if (!token) {
    throw new Error('No access token found. Please log in first.')
  }

  const response = await fetch(
    `${API_BASE_URL}/history/${analysisId}`,
    {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )

  if (!response.ok) {
    let message = 'Failed to delete analysis.'

    try {
      const data = await response.json()
      message = data.detail || message
    } catch {
      // No JSON error body
    }

    throw new Error(message)
  }

  return true
}

export async function getDashboardStats() {
  const token = localStorage.getItem('access_token')

  if (!token) {
    throw new Error('No access token found. Please log in first.')
  }

  const response = await fetch(
    `${API_BASE_URL}/dashboard/stats`,
    {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )

  const data = await response.json()

  if (!response.ok) {
    throw new Error(
      data.detail || 'Failed to load dashboard statistics.'
    )
  }

  return data
}