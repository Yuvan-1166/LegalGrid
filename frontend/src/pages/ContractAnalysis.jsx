import { useState } from 'react'
import { analyzeContract, analyzeContractFile } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorAlert from '../components/ErrorAlert'

export default function ContractAnalysis() {
  const [contractText, setContractText] = useState('')
  const [file, setFile] = useState(null)
  const [jurisdiction, setJurisdiction] = useState('All-India')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [mode, setMode] = useState('text')

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

  const getRiskLevel = (score) => {
    if (score > 70) return { label: 'High Risk', color: 'red', gradient: 'from-red-500 to-rose-600' }
    if (score > 40) return { label: 'Medium Risk', color: 'yellow', gradient: 'from-amber-500 to-orange-600' }
    return { label: 'Low Risk', color: 'green', gradient: 'from-emerald-500 to-green-600' }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Header with gradient accent */}
        <div className="mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium mb-4">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
              <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd"/>
            </svg>
            Contract Analysis
          </div>
          <h1 className="text-4xl font-bold text-slate-900 mb-3 tracking-tight">
            Analyze your contracts
          </h1>
          <p className="text-lg text-slate-600">
            AI-powered risk assessment and compliance checking for Indian law
          </p>
        </div>

        {/* Main Input Card with glassmorphism */}
        <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8 mb-8">
          {/* Segmented Control */}
          <div className="inline-flex p-1 bg-slate-100 rounded-xl mb-8">
            <button
              onClick={() => setMode('text')}
              className={`px-6 py-2.5 rounded-lg font-medium transition-all duration-200 ${
                mode === 'text'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Paste text
            </button>
            <button
              onClick={() => setMode('file')}
              className={`px-6 py-2.5 rounded-lg font-medium transition-all duration-200 ${
                mode === 'file'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Upload file
            </button>
          </div>

          {mode === 'text' ? (
            <div className="mb-6">
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Contract text
              </label>
              <textarea
                value={contractText}
                onChange={(e) => setContractText(e.target.value)}
                placeholder="Paste your contract text here..."
                className="w-full text-gray-900 h-72 p-5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-sm leading-relaxed transition-all"
              />
            </div>
          ) : (
            <div className="mb-6">
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Upload contract
              </label>
              <div className="relative border-2 border-dashed border-slate-300 rounded-xl p-12 text-center hover:border-blue-400 hover:bg-blue-50/50 transition-all duration-200 group">
                <input
                  type="file"
                  accept=".pdf,.txt"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  id="file-upload"
                />
                <div className="pointer-events-none">
                  <div className="w-16 h-16 mx-auto mb-4 bg-blue-100 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform">
                    <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>
                  {file ? (
                    <div>
                      <p className="text-blue-600 font-semibold mb-1">{file.name}</p>
                      <p className="text-sm text-slate-500">Click to change file</p>
                    </div>
                  ) : (
                    <div>
                      <p className="text-slate-700 font-semibold mb-1">Drop your file here or click to browse</p>
                      <p className="text-sm text-slate-500">PDF or TXT up to 10MB</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          <div className="flex gap-4">
            <div className="flex-1">
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Jurisdiction
              </label>
              <select
                value={jurisdiction}
                onChange={(e) => setJurisdiction(e.target.value)}
                className="w-full px-4 text-gray-900 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none bg-white cursor-pointer"
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
                className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:from-blue-700 hover:to-blue-800 disabled:from-slate-400 disabled:to-slate-400 disabled:cursor-not-allowed font-semibold shadow-lg shadow-blue-500/30 hover:shadow-xl hover:shadow-blue-500/40 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]"
              >
                {loading ? 'Analyzing...' : 'Analyze contract'}
              </button>
            </div>
          </div>
        </div>

        {error && (
          <div className="mb-8">
            <ErrorAlert error={error} onDismiss={() => setError(null)} />
          </div>
        )}

        {loading && (
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl p-16 text-center">
            <LoadingSpinner size="lg" text="Analyzing your contract..." />
          </div>
        )}

        {result && !loading && (
          <div className="space-y-6">
            {/* Risk Score Card with gradient */}
            <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 overflow-hidden">
              <div className={`h-2 bg-gradient-to-r ${getRiskLevel(result.overall_risk_score).gradient}`}></div>
              <div className="p-8">
                <div className="flex items-start justify-between mb-6">
                  <div className="flex-1">
                    <h2 className="text-2xl font-bold text-slate-900 mb-3">Analysis summary</h2>
                    <p className="text-slate-600 leading-relaxed">{result.summary}</p>
                  </div>
                  <div className={`ml-6 px-6 py-3 rounded-xl font-bold text-lg ${
                    getRiskLevel(result.overall_risk_score).color === 'red' ? 'bg-red-100 text-red-700' :
                    getRiskLevel(result.overall_risk_score).color === 'yellow' ? 'bg-amber-100 text-amber-700' :
                    'bg-emerald-100 text-emerald-700'
                  }`}>
                    {getRiskLevel(result.overall_risk_score).label}
                  </div>
                </div>
                
                <div className="flex items-center gap-4">
                  <span className="text-sm font-semibold text-slate-700">Risk score</span>
                  <div className="flex-1 bg-slate-100 rounded-full h-4 overflow-hidden">
                    <div
                      className={`h-4 rounded-full bg-gradient-to-r ${getRiskLevel(result.overall_risk_score).gradient} transition-all duration-1000 ease-out`}
                      style={{ width: `${result.overall_risk_score}%` }}
                    />
                  </div>
                  <span className="text-2xl font-bold text-slate-900 min-w-[80px] text-right">
                    {result.overall_risk_score}<span className="text-lg text-slate-500">/100</span>
                  </span>
                </div>
              </div>
            </div>

            {/* Clauses Grid */}
            <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">
                Clause analysis
                <span className="ml-3 text-lg font-normal text-slate-500">({result.clauses.length} clauses)</span>
              </h2>
              <div className="space-y-4">
                {result.clauses.map((clause, index) => (
                  <div key={index} className="group border border-slate-200 rounded-xl p-6 hover:border-blue-300 hover:shadow-lg transition-all duration-200">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center font-bold text-slate-700 group-hover:bg-blue-100 group-hover:text-blue-700 transition-colors">
                          {index + 1}
                        </div>
                        <h3 className="font-semibold text-slate-900">Clause {index + 1}</h3>
                      </div>
                      <span className={`px-4 py-1.5 rounded-full text-xs font-bold ${
                        clause.risk_score > 70 ? 'bg-red-100 text-red-700' :
                        clause.risk_score > 40 ? 'bg-amber-100 text-amber-700' :
                        'bg-emerald-100 text-emerald-700'
                      }`}>
                        {clause.risk_score}/100
                      </span>
                    </div>
                    
                    <p className="text-sm text-slate-700 mb-4 bg-slate-50 p-4 rounded-lg border-l-4 border-slate-300 leading-relaxed">
                      {clause.clause}
                    </p>

                    <div className="mb-4 bg-slate-50 rounded-full h-2 overflow-hidden">
                      <div
                        className={`h-2 rounded-full transition-all duration-500 ${
                          clause.risk_score > 70 ? 'bg-gradient-to-r from-red-500 to-rose-600' :
                          clause.risk_score > 40 ? 'bg-gradient-to-r from-amber-500 to-orange-600' :
                          'bg-gradient-to-r from-emerald-500 to-green-600'
                        }`}
                        style={{ width: `${clause.risk_score}%` }}
                      />
                    </div>

                    {clause.red_flags.length > 0 && (
                      <div className="mb-4 bg-red-50 p-4 rounded-xl border-l-4 border-red-500">
                        <h4 className="font-semibold text-red-800 mb-2 text-sm flex items-center gap-2">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                          Red flags
                        </h4>
                        <ul className="space-y-1.5">
                          {clause.red_flags.map((flag, i) => (
                            <li key={i} className="text-sm text-red-700 flex items-start gap-2">
                              <span className="text-red-400 mt-1">•</span>
                              <span>{flag}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {clause.recommendations.length > 0 && (
                      <div className="bg-blue-50 p-4 rounded-xl border-l-4 border-blue-500">
                        <h4 className="font-semibold text-blue-800 mb-2 text-sm flex items-center gap-2">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                          </svg>
                          Recommendations
                        </h4>
                        <ul className="space-y-1.5">
                          {clause.recommendations.map((rec, i) => (
                            <li key={i} className="text-sm text-blue-700 flex items-start gap-2">
                              <span className="text-blue-400 mt-1">•</span>
                              <span>{rec}</span>
                            </li>
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
    </div>
  )
}
