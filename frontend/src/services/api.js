import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Contract Analysis
export const analyzeContract = async (contractText, jurisdiction = 'All-India') => {
  const response = await api.post('/api/v1/contracts/analyze', {
    contract_text: contractText,
    jurisdiction,
  })
  return response.data
}

export const analyzeContractFile = async (file, jurisdiction = 'All-India') => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('jurisdiction', jurisdiction)
  
  const response = await api.post('/api/v1/contracts/analyze-file', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const exportContractPDF = async (analysisResult) => {
  const response = await api.post('/api/v1/contracts/export-pdf', analysisResult, {
    responseType: 'blob',
  })
  return response.data
}

// Case Law Search
export const searchCases = async (caseDescription, jurisdiction = 'All-India', topK = 5) => {
  const response = await api.post('/api/v1/cases/search', {
    case_description: caseDescription,
    jurisdiction,
    top_k: topK,
  })
  return response.data
}

export const analyzePrecedentStrength = async (caseDescription, jurisdiction = 'All-India', topK = 5) => {
  const response = await api.post('/api/v1/cases/analyze-strength', {
    case_description: caseDescription,
    jurisdiction,
    top_k: topK,
  })
  return response.data
}

// Qdrant Operations
export const initializeQdrant = async () => {
  const response = await api.post('/api/v1/qdrant/initialize')
  return response.data
}

export const searchDocuments = async (query, collection, jurisdiction = 'All-India', topK = 5) => {
  const response = await api.post('/api/v1/qdrant/search', {
    query,
    collection,
    jurisdiction,
    top_k: topK,
  })
  return response.data
}

// Health Check
export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}

// Compliance Checking
export const checkCompliance = async (orgProfile, regulations) => {
  const response = await api.post('/api/v1/compliance/check', {
    org_profile: orgProfile,
    regulations,
  })
  return response.data
}

export const detectRegulatoryChanges = async (regulation, lastCheckDate = null) => {
  const params = lastCheckDate ? { last_check_date: lastCheckDate } : {}
  const response = await api.get(`/api/v1/compliance/detect-changes/${regulation}`, { params })
  return response.data
}

// Dispute Mediation
export const mediateDispute = async (parties, narrative, claims, jurisdiction = 'All-India') => {
  const response = await api.post('/api/v1/disputes/mediate', {
    dispute: {
      parties,
      narrative,
      claims,
      jurisdiction,
    },
  })
  return response.data
}

export const evaluateOutcome = async (outcomeDescription, outcomeRationale, parsedClaims) => {
  const response = await api.post('/api/v1/disputes/evaluate-outcome', {
    outcome_description: outcomeDescription,
    outcome_rationale: outcomeRationale,
    parsed_claims: parsedClaims,
  })
  return response.data
}

// Chat with AI
export const chatWithAI = async (message, sessionId = null) => {
  const response = await api.post('/api/v1/chat/message', {
    message,
    session_id: sessionId,
  })
  return response.data
}

export const uploadChatDocument = async (file, query = '', sessionId = null) => {
  const formData = new FormData()
  formData.append('file', file)
  if (query) formData.append('query', query)
  if (sessionId) formData.append('session_id', sessionId)
  
  const response = await api.post('/api/v1/chat/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

// Session Management
export const listChatSessions = async (limit = 50) => {
  const response = await api.get('/api/v1/chat/sessions', { params: { limit } })
  return response.data
}

export const createChatSession = async (title = null) => {
  const response = await api.post('/api/v1/chat/sessions', { title })
  return response.data
}

export const getChatSession = async (sessionId) => {
  const response = await api.get(`/api/v1/chat/sessions/${sessionId}`)
  return response.data
}

export const deleteChatSession = async (sessionId) => {
  const response = await api.delete(`/api/v1/chat/sessions/${sessionId}`)
  return response.data
}

export const updateSessionTitle = async (sessionId, title) => {
  const response = await api.patch(`/api/v1/chat/sessions/${sessionId}/title`, { title })
  return response.data
}

export default api
