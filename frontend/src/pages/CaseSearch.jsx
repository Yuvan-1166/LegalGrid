import { useState } from 'react'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorAlert from '../components/ErrorAlert'
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
      const data = await searchCases(caseDescription, jurisdiction, topK)
      setResult(data)

      const analysis = await analyzePrecedentStrength(caseDescription, jurisdiction, topK)
      setStrengthAnalysis(analysis)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Search failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50/30 to-slate-50">
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-medium mb-4">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V16h2a1 1 0 110 2H7a1 1 0 110-2h2V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1z" clipRule="evenodd"/>
            </svg>
            Case Law Research
          </div>
          <h1 className="text-4xl font-bold text-slate-900 mb-3 tracking-tight">
            Search legal precedents
          </h1>
          <p className="text-lg text-slate-600">
            Find relevant Supreme Court and High Court judgments with intelligent semantic search
          </p>
        </div>

        {/* Search Card */}
        <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8 mb-8">
          <div className="mb-6">
            <label className="block text-sm font-semibold text-slate-700 mb-3">
              Case description or legal issue
            </label>
            <textarea
              value={caseDescription}
              onChange={(e) => setCaseDescription(e.target.value)}
              placeholder="Describe your case or legal issue... e.g., 'Employment contract termination without notice period'"
              className="w-full text-gray-900 h-40 p-5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none text-sm leading-relaxed transition-all"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Jurisdiction
              </label>
              <select
                value={jurisdiction}
                onChange={(e) => setJurisdiction(e.target.value)}
                className="w-full text-gray-900 px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent appearance-none bg-white cursor-pointer"
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
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Number of results
              </label>
              <select
                value={topK}
                onChange={(e) => setTopK(parseInt(e.target.value))}
                className="w-full text-gray-900 px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent appearance-none bg-white cursor-pointer"
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
                className="w-full px-6 py-3 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-xl hover:from-purple-700 hover:to-purple-800 disabled:from-slate-400 disabled:to-slate-400 disabled:cursor-not-allowed font-semibold shadow-lg shadow-purple-500/30 hover:shadow-xl hover:shadow-purple-500/40 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]"
              >
                {loading ? 'Searching...' : 'Search precedents'}
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
            <LoadingSpinner size="lg" text="Searching legal precedents..." />
          </div>
        )}

        {result && !loading && (
          <div className="space-y-6">
            {/* Strength Analysis */}
            {strengthAnalysis && (
              <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8">
                <h2 className="text-2xl font-bold text-slate-900 mb-6">Precedent strength</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className={`relative overflow-hidden rounded-xl p-6 ${
                    strengthAnalysis.analysis.strength === 'strong' ? 'bg-gradient-to-br from-emerald-500 to-green-600' :
                    strengthAnalysis.analysis.strength === 'moderate' ? 'bg-gradient-to-br from-amber-500 to-orange-600' :
                    'bg-gradient-to-br from-red-500 to-rose-600'
                  }`}>
                    <div className="relative z-10">
                      <div className="text-sm font-medium text-white/80 mb-2">Overall strength</div>
                      <div className="text-3xl font-bold text-white capitalize">
                        {strengthAnalysis.analysis.strength}
                      </div>
                    </div>
                    <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16"></div>
                  </div>
                  
                  <div className="relative overflow-hidden rounded-xl p-6 bg-gradient-to-br from-blue-500 to-indigo-600">
                    <div className="relative z-10">
                      <div className="text-sm font-medium text-white/80 mb-2">Supreme Court</div>
                      <div className="text-3xl font-bold text-white">{strengthAnalysis.analysis.supreme_court_cases}</div>
                    </div>
                    <div className="absolute bottom-0 right-0 w-24 h-24 bg-white/10 rounded-full -mr-12 -mb-12"></div>
                  </div>
                  
                  <div className="relative overflow-hidden rounded-xl p-6 bg-gradient-to-br from-purple-500 to-pink-600">
                    <div className="relative z-10">
                      <div className="text-sm font-medium text-white/80 mb-2">High Courts</div>
                      <div className="text-3xl font-bold text-white">{strengthAnalysis.analysis.high_court_cases}</div>
                    </div>
                    <div className="absolute top-0 left-0 w-20 h-20 bg-white/10 rounded-full -ml-10 -mt-10"></div>
                  </div>
                </div>
                <div className="mt-6 bg-slate-50 p-5 rounded-xl border-l-4 border-purple-500">
                  <p className="text-slate-700 leading-relaxed">{strengthAnalysis.analysis.recommendation}</p>
                </div>
              </div>
            )}

            {/* Precedents List */}
            <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">
                {result.precedents.length} relevant precedents
              </h2>
              <div className="space-y-5">
                {result.precedents.map((precedent, index) => (
                  <div key={index} className="group border border-slate-200 rounded-xl p-6 hover:border-purple-300 hover:shadow-lg transition-all duration-200">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-3">
                          <div className="w-8 h-8 rounded-lg bg-purple-100 flex items-center justify-center font-bold text-purple-700 group-hover:bg-purple-600 group-hover:text-white transition-colors">
                            {index + 1}
                          </div>
                          <h3 className="text-lg font-bold text-slate-900">{precedent.title}</h3>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-slate-600">
                          <span className="flex items-center gap-1.5">
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                            </svg>
                            {precedent.year}
                          </span>
                          <span className="text-slate-400">•</span>
                          <span className="flex items-center gap-1.5">
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                            </svg>
                            {precedent.court}
                          </span>
                        </div>
                      </div>
                      <div className="ml-6 text-right">
                        <div className="text-xs text-slate-500 mb-2">Relevance</div>
                        <div className="flex items-center gap-3">
                          <div className="w-24 bg-slate-100 rounded-full h-2 overflow-hidden">
                            <div
                              className={`h-2 rounded-full transition-all duration-500 ${
                                precedent.relevance_score > 0.7 ? 'bg-gradient-to-r from-emerald-500 to-green-600' :
                                precedent.relevance_score > 0.5 ? 'bg-gradient-to-r from-amber-500 to-orange-600' :
                                'bg-gradient-to-r from-orange-500 to-red-600'
                              }`}
                              style={{ width: `${precedent.relevance_score * 100}%` }}
                            />
                          </div>
                          <span className="text-lg font-bold text-slate-900">
                            {(precedent.relevance_score * 100).toFixed(0)}%
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="mb-4 bg-slate-50 p-4 rounded-xl border-l-4 border-slate-300">
                      <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Summary</h4>
                      <p className="text-sm text-slate-700 leading-relaxed">{precedent.summary}</p>
                    </div>

                    <div className="bg-blue-50 p-4 rounded-xl border-l-4 border-blue-400">
                      <h4 className="text-xs font-semibold text-blue-600 uppercase tracking-wide mb-2">Holding</h4>
                      <p className="text-sm text-blue-900 leading-relaxed">{precedent.holding}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {!result && !loading && !error && (
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl p-16 text-center">
            <div className="w-20 h-20 mx-auto mb-6 bg-purple-100 rounded-2xl flex items-center justify-center">
              <svg className="w-10 h-10 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-slate-900 mb-2">Start your search</h3>
            <p className="text-slate-600">
              Enter a case description to find relevant legal precedents
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
