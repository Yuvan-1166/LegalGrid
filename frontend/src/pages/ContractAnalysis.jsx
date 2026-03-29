import { useState } from 'react'
import { analyzeContract, analyzeContractFile } from '../services/api'

export default function ContractAnalysis() {
  const [contractText, setContractText] = useState('')
  const [file, setFile] = useState(null)
  const [jurisdiction, setJurisdiction] = useState('All-India')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [mode, setMode] = useState('text') // 'text' or 'file'

  const handleAnalyze = async () => {
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
    if (score > 70) return 'text-red-600 bg-red-50'
    if (score > 40) return 'text-yellow-600 bg-yellow-50'
    return 'text-green-600 bg-green-50'
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Contract Analysis</h1>

      {/* Input Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        {/* Mode Toggle */}
        <div className="flex gap-4 mb-4">
          <button
            onClick={() => setMode('text')}
            className={`px-4 py-2 rounded ${
              mode === 'text'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-200 text-gray-700'
            }`}
          >
            Text Input
          </button>
          <button
            onClick={() => setMode('file')}
            className={`px-4 py-2 rounded ${
              mode === 'file'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-200 text-gray-700'
            }`}
          >
            File Upload
          </button>
        </div>

        {mode === 'text' ? (
          <textarea
            value={contractText}
            onChange={(e) => setContractText(e.target.value)}
            placeholder="Paste your contract text here..."
            className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
        ) : (
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
            <input
              type="file"
              accept=".pdf,.txt"
              onChange={(e) => setFile(e.target.files[0])}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="cursor-pointer text-indigo-600 hover:text-indigo-700"
            >
              {file ? (
                <span className="text-gray-900">{file.name}</span>
              ) : (
                <span>Click to upload PDF or TXT file</span>
              )}
            </label>
          </div>
        )}

        <div className="mt-4 flex gap-4 items-center">
          <select
            value={jurisdiction}
            onChange={(e) => setJurisdiction(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
          >
            <option value="All-India">All India</option>
            <option value="Delhi">Delhi</option>
            <option value="Mumbai">Mumbai</option>
            <option value="Bangalore">Bangalore</option>
          </select>

          <button
            onClick={handleAnalyze}
            disabled={loading || (mode === 'text' ? !contractText : !file)}
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Analyzing...' : 'Analyze Contract'}
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Results Display */}
      {result && (
        <div className="space-y-6">
          {/* Overall Summary */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4">Analysis Summary</h2>
            <div className="flex items-center gap-4 mb-4">
              <span className="text-lg font-medium">Overall Risk Score:</span>
              <span
                className={`text-2xl font-bold px-4 py-2 rounded ${getRiskColor(
                  result.overall_risk_score
                )}`}
              >
                {result.overall_risk_score}/100
              </span>
            </div>
            <p className="text-gray-700">{result.summary}</p>
          </div>

          {/* Clause Analysis */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4">Clause Analysis</h2>
            <div className="space-y-4">
              {result.clauses.map((clause, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-gray-900">
                      Clause {index + 1}
                    </h3>
                    <span
                      className={`px-3 py-1 rounded text-sm font-medium ${getRiskColor(
                        clause.risk_score
                      )}`}
                    >
                      Risk: {clause.risk_score}/100
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm mb-3">{clause.clause}</p>

                  {clause.red_flags.length > 0 && (
                    <div className="mb-3">
                      <h4 className="font-medium text-red-700 mb-1">Red Flags:</h4>
                      <ul className="list-disc list-inside text-sm text-gray-700">
                        {clause.red_flags.map((flag, i) => (
                          <li key={i}>{flag}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {clause.recommendations.length > 0 && (
                    <div>
                      <h4 className="font-medium text-green-700 mb-1">
                        Recommendations:
                      </h4>
                      <ul className="list-disc list-inside text-sm text-gray-700">
                        {clause.recommendations.map((rec, i) => (
                          <li key={i}>{rec}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
