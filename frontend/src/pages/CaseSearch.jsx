import { useState } from 'react'
import Card from '../components/Card'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorAlert from '../components/ErrorAlert'
import Badge from '../components/Badge'
import Tooltip from '../components/Tooltip'
import ProgressBar from '../components/ProgressBar'
import { searchCases, analyzePrecedentStrength } from '../services/api'

export default function CaseSearch() {
  const [caseDescription, setCaseDescription] = useState('')
  const [jurisdiction, setJurisdiction] = useState('All-India')
  const [topK, setTopK] = useState(5)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [strengthAnalysis, setStrengthAnalysis] = useState(null)
  const [error, setError] = useState(null)

  const handleSearch = async () => {
    if (!caseDescription.trim()) {
      setError('Please enter a case description')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)
    setStrengthAnalysis(null)

    try {
      // Search for precedents
      const data = await searchCases(caseDescription, jurisdiction, topK)
      setResult(data)

      // Analyze precedent strength
      const analysis = await analyzePrecedentStrength(caseDescription, jurisdiction, topK)
      setStrengthAnalysis(analysis)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Search failed')
    } finally {
      setLoading(false)
    }
  }

  const getStrengthColor = (strength) => {
    if (strength === 'strong') return 'bg-green-100 text-green-800 border-green-300'
    if (strength === 'moderate') return 'bg-yellow-100 text-yellow-800 border-yellow-300'
    return 'bg-red-100 text-red-800 border-red-300'
  }

  const getRelevanceColor = (score) => {
    if (score > 0.7) return 'bg-green-500'
    if (score > 0.5) return 'bg-yellow-500'
    return 'bg-orange-500'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Case Law Search</h1>
          <p className="text-lg text-gray-600">
            Find relevant legal precedents from Supreme Court and High Courts
          </p>
        </div>

        {/* Search Section */}
        <Card className="mb-6">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Case Description or Legal Issue
            </label>
            <textarea
              value={caseDescription}
              onChange={(e) => setCaseDescription(e.target.value)}
              placeholder="Describe your case or legal issue... e.g., 'Employment contract termination without notice period'"
              className="w-full h-40 p-4 border-2 text-gray-900 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Jurisdiction
              </label>
              <select
                value={jurisdiction}
                onChange={(e) => setJurisdiction(e.target.value)}
                className="w-full px-4 py-2 text-gray-900 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="All-India">All India</option>
                <option value="Supreme Court">Supreme Court</option>
                <option value="Delhi">Delhi High Court</option>
                <option value="Mumbai">Mumbai High Court</option>
                <option value="Bangalore">Bangalore High Court</option>
                <option value="Chennai">Chennai High Court</option>
                <option value="Kolkata">Kolkata High Court</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Results
              </label>
              <select
                value={topK}
                onChange={(e) => setTopK(parseInt(e.target.value))}
                className="w-full px-4 py-2 text-gray-900 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="3">3 precedents</option>
                <option value="5">5 precedents</option>
                <option value="10">10 precedents</option>
                <option value="15">15 precedents</option>
              </select>
            </div>

            <div className="flex items-end">
              <button
                onClick={handleSearch}
                disabled={loading}
                className="w-full px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium shadow-md hover:shadow-lg transition-all"
              >
                {loading ? 'Searching...' : '🔍 Search Precedents'}
              </button>
            </div>
          </div>
        </Card>

        {/* Error Display */}
        {error && (
          <div className="mb-6">
            <ErrorAlert error={error} onDismiss={() => setError(null)} />
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <Card className="mb-6">
            <LoadingSpinner size="lg" text="Searching legal precedents..." />
          </Card>
        )}

        {/* Results Display */}
        {result && !loading && (
          <div className="space-y-6 animate-fade-in">
            {/* Strength Analysis */}
            {strengthAnalysis && (
              <Card>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Precedent Strength Analysis</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                  <div className={`p-4 rounded-lg border-2 ${getStrengthColor(strengthAnalysis.analysis.strength)}`}>
                    <div className="text-sm font-medium mb-1">Overall Strength</div>
                    <div className="text-2xl font-bold uppercase">{strengthAnalysis.analysis.strength}</div>
                  </div>
                  <div className="p-4 rounded-lg border-2 bg-blue-50 text-blue-800 border-blue-300">
                    <div className="text-sm font-medium mb-1">Supreme Court Cases</div>
                    <div className="text-2xl font-bold">{strengthAnalysis.analysis.supreme_court_cases}</div>
                  </div>
                  <div className="p-4 rounded-lg border-2 bg-indigo-50 text-indigo-800 border-indigo-300">
                    <div className="text-sm font-medium mb-1">High Court Cases</div>
                    <div className="text-2xl font-bold">{strengthAnalysis.analysis.high_court_cases}</div>
                  </div>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg border-l-4 border-purple-500">
                  <p className="text-gray-800">{strengthAnalysis.analysis.recommendation}</p>
                </div>
              </Card>
            )}

            {/* Precedents List */}
            <Card>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Found {result.precedents.length} Relevant Precedents
              </h2>
              <div className="space-y-4">
                {result.precedents.map((precedent, index) => (
                  <div
                    key={index}
                    className="border-2 border-gray-200 rounded-lg p-5 hover:border-purple-300 hover:shadow-md transition-all"
                  >
                    {/* Header */}
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-2xl font-bold text-purple-600">#{index + 1}</span>
                          <h3 className="text-lg font-bold text-gray-900">{precedent.title}</h3>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-gray-600">
                          <span className="flex items-center gap-1">
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                            </svg>
                            {precedent.year}
                          </span>
                          <span className="flex items-center gap-1">
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                            </svg>
                            {precedent.court}
                          </span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-xs text-gray-500 mb-1">Relevance</div>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full ${getRelevanceColor(precedent.relevance_score)}`}
                              style={{ width: `${precedent.relevance_score * 100}%` }}
                            />
                          </div>
                          <span className="text-sm font-bold text-gray-700">
                            {(precedent.relevance_score * 100).toFixed(0)}%
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Summary */}
                    <div className="mb-3 bg-gray-50 p-3 rounded border-l-4 border-purple-300">
                      <h4 className="text-sm font-semibold text-gray-700 mb-1">Summary</h4>
                      <p className="text-sm text-gray-700">{precedent.summary}</p>
                    </div>

                    {/* Holding */}
                    <div className="mb-3 bg-blue-50 p-3 rounded border-l-4 border-blue-400">
                      <h4 className="text-sm font-semibold text-blue-800 mb-1">Holding</h4>
                      <p className="text-sm text-blue-900">{precedent.holding}</p>
                    </div>

                    {/* Reason Retrieved */}
                    <div className="text-xs text-gray-600 bg-purple-50 p-2 rounded">
                      <span className="font-medium">Why retrieved:</span> {precedent.reason_retrieved}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}

        {/* Empty State */}
        {!result && !loading && !error && (
          <Card className="text-center py-12">
            <svg
              className="w-16 h-16 text-gray-400 mx-auto mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No search yet</h3>
            <p className="text-gray-600">
              Enter a case description above to find relevant legal precedents
            </p>
          </Card>
        )}
      </div>
    </div>
  )
}
