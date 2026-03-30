import { useState } from 'react'
import { analyzeContract, analyzeContractFile } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorAlert from '../components/ErrorAlert'
import Card from '../components/Card'
import ProgressBar from '../components/ProgressBar'
import Badge from '../components/Badge'
import Tooltip from '../components/Tooltip'

export default function ContractAnalysis() {
  const [contractText, setContractText] = useState('')
  const [file, setFile] = useState(null)
  const [jurisdiction, setJurisdiction] = useState('All-India')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [mode, setMode] = useState('text') // 'text' or 'file'

  const handleAnalyze = async () => {
    if (mode === 'text' && !contractText.trim()) {
      setError('Please enter contract text')
      return
    }
    if (mode === 'file' && !file) {
      setError('Please select a file')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      let data
      if (mode === 'text') {
        data = await analyzeContract(contractText, jurisdiction)
      } else {
        data = await analyzeContractFile(file, jurisdiction)
      }
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (score) => {
    if (score > 70) return 'text-red-600 bg-red-50 border-red-200'
    if (score > 40) return 'text-yellow-600 bg-yellow-50 border-yellow-200'
    return 'text-green-600 bg-green-50 border-green-200'
  }

  const getRiskBadge = (score) => {
    if (score > 70) return { text: 'HIGH RISK', color: 'bg-red-500' }
    if (score > 40) return { text: 'MEDIUM RISK', color: 'bg-yellow-500' }
    return { text: 'LOW RISK', color: 'bg-green-500' }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Contract Analysis</h1>
          <p className="text-lg text-gray-600">
            AI-powered risk assessment and compliance checking for Indian law
          </p>
        </div>

        {/* Input Section */}
        <Card className="mb-6">
          {/* Mode Toggle */}
          <div className="flex gap-2 mb-6">
            <button
              onClick={() => setMode('text')}
              className={`flex-1 px-6 py-3 rounded-lg font-medium transition-all ${
                mode === 'text'
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              📝 Text Input
            </button>
            <button
              onClick={() => setMode('file')}
              className={`flex-1 px-6 py-3 rounded-lg font-medium transition-all ${
                mode === 'file'
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              📄 File Upload
            </button>
          </div>

          {mode === 'text' ? (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Contract Text
              </label>
              <textarea
                value={contractText}
                onChange={(e) => setContractText(e.target.value)}
                placeholder="Paste your contract text here..."
                className="w-full h-64 p-4 border-2 text-gray-900 placeholder-gray-500 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none font-mono text-sm"
              />
            </div>
          ) : (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Upload Contract
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-indigo-400 transition-colors">
                <input
                  type="file"
                  accept=".pdf,.txt"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer flex flex-col items-center"
                >
                  <svg
                    className="w-12 h-12 text-gray-400 mb-3"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                    />
                  </svg>
                  {file ? (
                    <div>
                      <span className="text-indigo-600 font-medium">{file.name}</span>
                      <p className="text-sm text-gray-500 mt-1">Click to change file</p>
                    </div>
                  ) : (
                    <div>
                      <span className="text-indigo-600 font-medium">Click to upload</span>
                      <p className="text-sm text-gray-500 mt-1">PDF or TXT (max 10MB)</p>
                    </div>
                  )}
                </label>
              </div>
            </div>
          )}

          <div className="flex gap-4 items-center">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Jurisdiction
              </label>
              <select
                value={jurisdiction}
                onChange={(e) => setJurisdiction(e.target.value)}
                className="w-full px-4 py-2 text-gray-900 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="All-India">All India</option>
                <option value="Delhi">Delhi</option>
                <option value="Mumbai">Mumbai</option>
                <option value="Bangalore">Bangalore</option>
                <option value="Chennai">Chennai</option>
                <option value="Kolkata">Kolkata</option>
              </select>
            </div>

            <div className="flex-1 flex items-end">
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="w-full px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium shadow-md hover:shadow-lg transition-all"
              >
                {loading ? 'Analyzing...' : '🔍 Analyze Contract'}
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
            <LoadingSpinner size="lg" text="Analyzing contract with AI..." />
          </Card>
        )}

        {/* Results Display */}
        {result && !loading && (
          <div className="space-y-6 animate-fade-in">
            {/* Overall Summary */}
            <Card>
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Analysis Summary</h2>
                  <p className="text-gray-600">{result.summary}</p>
                </div>
                <div className="text-right">
                  <Badge 
                    variant={result.overall_risk_score > 70 ? 'danger' : result.overall_risk_score > 40 ? 'warning' : 'success'}
                    size="lg"
                  >
                    {getRiskBadge(result.overall_risk_score).text}
                  </Badge>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Tooltip content="Overall risk assessment based on all clauses" position="top">
                    <span className="text-lg font-medium text-gray-700 cursor-help">
                      Overall Risk Score
                    </span>
                  </Tooltip>
                  <span className={`text-2xl font-bold px-4 py-2 rounded-lg border-2 ${getRiskColor(result.overall_risk_score)}`}>
                    {result.overall_risk_score}/100
                  </span>
                </div>
                <ProgressBar 
                  value={result.overall_risk_score} 
                  max={100}
                  color={result.overall_risk_score > 70 ? 'red' : result.overall_risk_score > 40 ? 'yellow' : 'green'}
                />
              </div>
            </Card>

            {/* Clause Analysis */}
            <Card>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Detailed Clause Analysis ({result.clauses.length} clauses)
              </h2>
              <div className="space-y-4">
                {result.clauses.map((clause, index) => (
                  <div
                    key={index}
                    className="border-2 border-gray-200 rounded-lg p-5 hover:border-indigo-300 transition-colors"
                  >
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="font-semibold text-gray-900 text-lg">
                        Clause {index + 1}
                      </h3>
                      <Badge 
                        variant={clause.risk_score > 70 ? 'danger' : clause.risk_score > 40 ? 'warning' : 'success'}
                      >
                        Risk: {clause.risk_score}/100
                      </Badge>
                    </div>
                    
                    <p className="text-gray-700 text-sm mb-4 bg-gray-50 p-3 rounded border-l-4 border-gray-300">
                      {clause.clause}
                    </p>

                    <div className="mb-3">
                      <ProgressBar 
                        value={clause.risk_score} 
                        max={100}
                        label="Risk Level"
                        color={clause.risk_score > 70 ? 'red' : clause.risk_score > 40 ? 'yellow' : 'green'}
                      />
                    </div>

                    {clause.red_flags.length > 0 && (
                      <div className="mb-4 bg-red-50 p-4 rounded-lg border-l-4 border-red-500">
                        <h4 className="font-medium text-red-800 mb-2 flex items-center gap-2">
                          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                          Red Flags
                        </h4>
                        <ul className="list-disc list-inside text-sm text-red-700 space-y-1">
                          {clause.red_flags.map((flag, i) => (
                            <li key={i}>{flag}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {clause.recommendations.length > 0 && (
                      <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                        <h4 className="font-medium text-green-800 mb-2 flex items-center gap-2">
                          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                          </svg>
                          Recommendations
                        </h4>
                        <ul className="list-disc list-inside text-sm text-green-700 space-y-1">
                          {clause.recommendations.map((rec, i) => (
                            <li key={i}>{rec}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}
