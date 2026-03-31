import { useState } from 'react'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorAlert from '../components/ErrorAlert'
import { mediateDispute } from '../services/api'

export default function Disputes() {
  const [parties, setParties] = useState(['', ''])
  const [narrative, setNarrative] = useState('')
  const [claims, setClaims] = useState([''])
  const [jurisdiction, setJurisdiction] = useState('All-India')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const addParty = () => setParties([...parties, ''])
  const updateParty = (index, value) => {
    const newParties = [...parties]
    newParties[index] = value
    setParties(newParties)
  }
  const removeParty = (index) => {
    if (parties.length > 2) setParties(parties.filter((_, i) => i !== index))
  }

  const addClaim = () => setClaims([...claims, ''])
  const updateClaim = (index, value) => {
    const newClaims = [...claims]
    newClaims[index] = value
    setClaims(newClaims)
  }
  const removeClaim = (index) => {
    if (claims.length > 1) setClaims(claims.filter((_, i) => i !== index))
  }

  const handleMediate = async () => {
    const validParties = parties.filter(p => p.trim())
    const validClaims = claims.filter(c => c.trim())

    if (validParties.length < 2) {
      setError('Please enter at least 2 parties')
      return
    }

    if (!narrative.trim()) {
      setError('Please describe the dispute')
      return
    }

    if (validClaims.length === 0) {
      setError('Please enter at least one claim')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await mediateDispute(validParties, narrative, validClaims, jurisdiction)
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Mediation failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-orange-50/30 to-slate-50">
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-orange-100 text-orange-700 rounded-full text-sm font-medium mb-4">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd"/>
            </svg>
            Dispute Mediation
          </div>
          <h1 className="text-4xl font-bold text-slate-900 mb-3 tracking-tight">
            Resolve disputes fairly
          </h1>
          <p className="text-lg text-slate-600">
            AI-powered mediation for multi-party disputes with fair outcome generation
          </p>
        </div>

        {/* Input Card */}
        <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8 mb-8">
          <h2 className="text-xl font-bold text-slate-900 mb-6">Dispute details</h2>

          <div className="mb-6">
            <label className="block text-sm font-semibold text-slate-700 mb-3">
              Parties involved
            </label>
            <div className="space-y-3">
              {parties.map((party, index) => (
                <div key={index} className="flex gap-3">
                  <input
                    type="text"
                    value={party}
                    onChange={(e) => updateParty(index, e.target.value)}
                    placeholder={`Party ${index + 1} name`}
                    className="flex-1 px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                  />
                  {parties.length > 2 && (
                    <button
                      onClick={() => removeParty(index)}
                      className="px-4 py-2 bg-red-100 text-red-600 rounded-xl hover:bg-red-200 font-medium transition-colors"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
            </div>
            <button
              onClick={addParty}
              className="mt-3 px-4 py-2 bg-slate-100 text-slate-700 rounded-xl hover:bg-slate-200 font-medium transition-colors flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd"/>
              </svg>
              Add party
            </button>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-semibold text-slate-700 mb-3">
              Dispute narrative
            </label>
            <textarea
              value={narrative}
              onChange={(e) => setNarrative(e.target.value)}
              placeholder="Describe the dispute in detail... e.g., 'Property dispute between siblings over inherited land...'"
              className="w-full h-40 p-5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none text-sm leading-relaxed transition-all"
            />
          </div>

          <div className="mb-6">
            <label className="block text-sm font-semibold text-slate-700 mb-3">
              Claims made
            </label>
            <div className="space-y-3">
              {claims.map((claim, index) => (
                <div key={index} className="flex gap-3">
                  <input
                    type="text"
                    value={claim}
                    onChange={(e) => updateClaim(index, e.target.value)}
                    placeholder={`Claim ${index + 1}`}
                    className="flex-1 px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                  />
                  {claims.length > 1 && (
                    <button
                      onClick={() => removeClaim(index)}
                      className="px-4 py-2 bg-red-100 text-red-600 rounded-xl hover:bg-red-200 font-medium transition-colors"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
            </div>
            <button
              onClick={addClaim}
              className="mt-3 px-4 py-2 bg-slate-100 text-slate-700 rounded-xl hover:bg-slate-200 font-medium transition-colors flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd"/>
              </svg>
              Add claim
            </button>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-semibold text-slate-700 mb-3">
              Jurisdiction
            </label>
            <select
              value={jurisdiction}
              onChange={(e) => setJurisdiction(e.target.value)}
              className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent appearance-none bg-white cursor-pointer"
            >
              <option value="All-India">All India</option>
              <option value="Delhi">Delhi</option>
              <option value="Mumbai">Mumbai</option>
              <option value="Bangalore">Bangalore</option>
              <option value="Chennai">Chennai</option>
              <option value="Kolkata">Kolkata</option>
            </select>
          </div>

          <button
            onClick={handleMediate}
            disabled={loading}
            className="w-full px-6 py-3 bg-gradient-to-r from-orange-600 to-orange-700 text-white rounded-xl hover:from-orange-700 hover:to-orange-800 disabled:from-slate-400 disabled:to-slate-400 disabled:cursor-not-allowed font-semibold shadow-lg shadow-orange-500/30 hover:shadow-xl hover:shadow-orange-500/40 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]"
          >
            {loading ? 'Analyzing...' : 'Mediate dispute'}
          </button>
        </div>

        {error && (
          <div className="mb-8">
            <ErrorAlert error={error} onDismiss={() => setError(null)} />
          </div>
        )}

        {loading && (
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl p-16 text-center">
            <LoadingSpinner size="lg" text="Analyzing dispute..." />
          </div>
        )}

        {result && !loading && (
          <div className="space-y-6">
            {/* Parsed Claims */}
            <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">Parsed claims by party</h2>
              <div className="space-y-5">
                {Object.entries(result.parsed_claims).map(([party, data], index) => (
                  <div key={index} className="border border-slate-200 rounded-xl p-6 hover:border-orange-300 hover:shadow-lg transition-all duration-200">
                    <h3 className="text-lg font-bold text-orange-600 mb-4">{party}</h3>
                    
                    <div className="mb-4">
                      <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Claims</h4>
                      <ul className="space-y-2">
                        {data.claims.map((claim, idx) => (
                          <li key={idx} className="text-sm text-slate-700 flex items-start gap-2">
                            <span className="text-orange-400 mt-1">•</span>
                            <span>{claim}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="mb-4">
                      <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Interests</h4>
                      <ul className="space-y-2">
                        {data.interests.map((interest, idx) => (
                          <li key={idx} className="text-sm text-slate-700 flex items-start gap-2">
                            <span className="text-orange-400 mt-1">•</span>
                            <span>{interest}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="bg-blue-50 p-4 rounded-xl border-l-4 border-blue-400">
                      <h4 className="text-xs font-semibold text-blue-600 uppercase tracking-wide mb-2">Desired outcome</h4>
                      <p className="text-sm text-blue-900 leading-relaxed">{data.desired_outcome}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Common Ground */}
            <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">Common ground analysis</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-green-50 p-5 rounded-xl border-l-4 border-green-500">
                  <h3 className="text-sm font-semibold text-green-800 mb-3 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                    </svg>
                    Agreements
                  </h3>
                  <ul className="space-y-2">
                    {result.common_ground.agreements.map((item, idx) => (
                      <li key={idx} className="text-sm text-green-900 flex items-start gap-2">
                        <span className="text-green-400 mt-1">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-red-50 p-5 rounded-xl border-l-4 border-red-500">
                  <h3 className="text-sm font-semibold text-red-800 mb-3 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
                    </svg>
                    Conflicts
                  </h3>
                  <ul className="space-y-2">
                    {result.common_ground.conflicts.map((item, idx) => (
                      <li key={idx} className="text-sm text-red-900 flex items-start gap-2">
                        <span className="text-red-400 mt-1">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-blue-50 p-5 rounded-xl border-l-4 border-blue-500">
                  <h3 className="text-sm font-semibold text-blue-800 mb-3 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd"/>
                    </svg>
                    Opportunities
                  </h3>
                  <ul className="space-y-2">
                    {result.common_ground.compromise_opportunities.map((item, idx) => (
                      <li key={idx} className="text-sm text-blue-900 flex items-start gap-2">
                        <span className="text-blue-400 mt-1">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Proposed Outcomes */}
            <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">Proposed outcomes</h2>
              <div className="space-y-5">
                {result.proposed_outcomes.map((outcome, index) => (
                  <div key={index} className="group border border-slate-200 rounded-xl p-6 hover:border-orange-300 hover:shadow-lg transition-all duration-200">
                    <div className="flex items-center gap-3 mb-4">
                      <div className="w-8 h-8 rounded-lg bg-orange-100 flex items-center justify-center font-bold text-orange-700 group-hover:bg-orange-600 group-hover:text-white transition-colors">
                        {index + 1}
                      </div>
                      <span className={`px-4 py-1.5 rounded-full text-xs font-bold ${
                        outcome.outcome_type === 'compromise' ? 'bg-blue-100 text-blue-700' :
                        outcome.outcome_type === 'precedent' ? 'bg-purple-100 text-purple-700' :
                        'bg-green-100 text-green-700'
                      }`}>
                        {outcome.outcome_type.toUpperCase()}
                      </span>
                    </div>

                    <div className="mb-4 bg-slate-50 p-5 rounded-xl border-l-4 border-slate-300">
                      <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Outcome</h4>
                      <p className="text-slate-800 leading-relaxed">{outcome.description}</p>
                    </div>

                    <div className="bg-blue-50 p-5 rounded-xl border-l-4 border-blue-400">
                      <h4 className="text-xs font-semibold text-blue-600 uppercase tracking-wide mb-2">Rationale</h4>
                      <p className="text-sm text-blue-900 leading-relaxed">{outcome.rationale}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Relevant Precedents */}
            {result.precedents && result.precedents.length > 0 && (
              <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8">
                <h2 className="text-2xl font-bold text-slate-900 mb-6">Relevant precedents</h2>
                <div className="space-y-4">
                  {result.precedents.map((precedent, index) => (
                    <div key={index} className="border border-slate-200 rounded-xl p-5 hover:border-orange-300 transition-all">
                      <h3 className="font-bold text-slate-900 mb-2">{precedent.title}</h3>
                      <p className="text-sm text-slate-700 leading-relaxed mb-2">{precedent.content}</p>
                      <div className="text-xs text-slate-500">
                        Relevance: {(precedent.score * 100).toFixed(0)}%
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {!result && !loading && !error && (
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl p-16 text-center">
            <div className="w-20 h-20 mx-auto mb-6 bg-orange-100 rounded-2xl flex items-center justify-center">
              <svg className="w-10 h-10 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-slate-900 mb-2">Start mediation</h3>
            <p className="text-slate-600">
              Enter dispute details to get AI-powered mediation suggestions
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
