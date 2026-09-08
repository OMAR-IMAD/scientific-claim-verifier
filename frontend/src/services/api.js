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