import { useState } from 'react'
import Card from '../components/Card'
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

  const addParty = () => {
    setParties([...parties, ''])
  }

  const updateParty = (index, value) => {
    const newParties = [...parties]
    newParties[index] = value
    setParties(newParties)
  }

  const removeParty = (index) => {
    if (parties.length > 2) {
      setParties(parties.filter((_, i) => i !== index))
    }
  }

  const addClaim = () => {
    setClaims([...claims, ''])
  }

  const updateClaim = (index, value) => {
    const newClaims = [...claims]
    newClaims[index] = value
    setClaims(newClaims)
  }

  const removeClaim = (index) => {
    if (claims.length > 1) {
      setClaims(claims.filter((_, i) => i !== index))
    }
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

  const getOutcomeTypeColor = (type) => {
    if (type === 'compromise') return 'bg-blue-100 text-blue-800 border-blue-300'
    if (type === 'precedent') return 'bg-purple-100 text-purple-800 border-purple-300'
    if (type === 'interest') return 'bg-green-100 text-green-800 border-green-300'
    return 'bg-gray-100 text-gray-800 border-gray-300'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Dispute Mediation</h1>
          <p className="text-lg text-gray-600">
            AI-powered mediation for multi-party disputes
          </p>
        </div>

        {/* Input Section */}
        <Card className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Dispute Details</h2>

          {/* Parties */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Parties Involved
            </label>
            {parties.map((party, index) => (
              <div key={index} className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={party}
                  onChange={(e) => updateParty(index, e.target.value)}
                  placeholder={`Party ${index + 1} name`}
                  className="flex-1 px-4 py-2 text-gray-900 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
                {parties.length > 2 && (
                  <button
                    onClick={() => removeParty(index)}
                    className="px-4 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200"
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}
            <button
              onClick={addParty}
              className="mt-2 px-4 py-2 bg-orange-100 text-orange-700 rounded-lg hover:bg-orange-200 font-medium"
            >
              + Add Party
            </button>
          </div>

          {/* Narrative */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dispute Narrative
            </label>
            <textarea
              value={narrative}
              onChange={(e) => setNarrative(e.target.value)}
              placeholder="Describe the dispute in detail... e.g., 'Property dispute between siblings over inherited land. Party A claims 60% ownership based on contribution, Party B claims equal split...'"
              className="w-full h-40 p-4 border-2 text-gray-900 border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
            />
          </div>

          {/* Claims */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Claims Made
            </label>
            {claims.map((claim, index) => (
              <div key={index} className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={claim}
                  onChange={(e) => updateClaim(index, e.target.value)}
                  placeholder={`Claim ${index + 1}`}
                  className="flex-1 px-4 py-2 text-gray-900 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
                {claims.length > 1 && (
                  <button
                    onClick={() => removeClaim(index)}
                    className="px-4 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200"
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}
            <button
              onClick={addClaim}
              className="mt-2 px-4 py-2 bg-orange-100 text-orange-700 rounded-lg hover:bg-orange-200 font-medium"
            >
              + Add Claim
            </button>
          </div>

          {/* Jurisdiction */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Jurisdiction
            </label>
            <select
              value={jurisdiction}
              onChange={(e) => setJurisdiction(e.target.value)}
              className="w-full px-4 py-2 text-gray-900 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
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
            className="w-full px-6 py-3 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium shadow-md hover:shadow-lg transition-all"
          >
            {loading ? 'Analyzing Dispute...' : '⚖️ Mediate Dispute'}
          </button>
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
            <LoadingSpinner size="lg" text="Analyzing dispute and generating fair outcomes..." />
          </Card>
        )}

        {/* Results Display */}
        {result && !loading && (
          <div className="space-y-6 animate-fade-in">
            {/* Parsed Claims */}
            <Card>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Parsed Claims by Party</h2>
              <div className="space-y-4">
                {Object.entries(result.parsed_claims).map(([party, data], index) => (
                  <div
                    key={index}
                    className="border-2 border-gray-200 rounded-lg p-4 hover:border-orange-300 transition-all"
                  >
                    <h3 className="text-lg font-bold text-orange-600 mb-3">{party}</h3>
                    
                    <div className="mb-3">
                      <h4 className="text-sm font-semibold text-gray-700 mb-1">Claims:</h4>
                      <ul className="list-disc list-inside space-y-1">
                        {data.claims.map((claim, idx) => (
                          <li key={idx} className="text-sm text-gray-700">{claim}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="mb-3">
                      <h4 className="text-sm font-semibold text-gray-700 mb-1">Interests:</h4>
                      <ul className="list-disc list-inside space-y-1">
                        {data.interests.map((interest, idx) => (
                          <li key={idx} className="text-sm text-gray-700">{interest}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="bg-orange-50 p-3 rounded">
                      <h4 className="text-sm font-semibold text-orange-800 mb-1">Desired Outcome:</h4>
                      <p className="text-sm text-orange-900">{data.desired_outcome}</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            {/* Common Ground */}
            <Card>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Common Ground Analysis</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                  <h3 className="text-sm font-semibold text-green-800 mb-2">Agreements</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {result.common_ground.agreements.map((item, idx) => (
                      <li key={idx} className="text-sm text-green-900">{item}</li>
                    ))}
                  </ul>
                </div>

                <div className="bg-red-50 p-4 rounded-lg border-l-4 border-red-500">
                  <h3 className="text-sm font-semibold text-red-800 mb-2">Conflicts</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {result.common_ground.conflicts.map((item, idx) => (
                      <li key={idx} className="text-sm text-red-900">{item}</li>
                    ))}
                  </ul>
                </div>

                <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                  <h3 className="text-sm font-semibold text-blue-800 mb-2">Compromise Opportunities</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {result.common_ground.compromise_opportunities.map((item, idx) => (
                      <li key={idx} className="text-sm text-blue-900">{item}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </Card>

            {/* Proposed Outcomes */}
            <Card>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Proposed Fair Outcomes</h2>
              <div className="space-y-4">
                {result.proposed_outcomes.map((outcome, index) => (
                  <div
                    key={index}
                    className="border-2 border-gray-200 rounded-lg p-5 hover:border-orange-300 hover:shadow-md transition-all"
                  >
                    <div className="flex items-center gap-3 mb-3">
                      <span className="text-2xl font-bold text-orange-600">#{index + 1}</span>
                      <span className={`px-3 py-1 rounded-full text-xs font-bold border-2 ${getOutcomeTypeColor(outcome.outcome_type)}`}>
                        {outcome.outcome_type.toUpperCase()}
                      </span>
                    </div>

                    <div className="mb-3 bg-gray-50 p-4 rounded border-l-4 border-orange-400">
                      <h4 className="text-sm font-semibold text-gray-700 mb-2">Outcome Description</h4>
                      <p className="text-gray-800">{outcome.description}</p>
                    </div>

                    <div className="bg-blue-50 p-4 rounded border-l-4 border-blue-400">
                      <h4 className="text-sm font-semibold text-blue-800 mb-2">Rationale</h4>
                      <p className="text-sm text-blue-900">{outcome.rationale}</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            {/* Relevant Precedents */}
            {result.precedents && result.precedents.length > 0 && (
              <Card>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Relevant Legal Precedents</h2>
                <div className="space-y-3">
                  {result.precedents.map((precedent, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded-lg p-4 hover:border-orange-300 transition-all"
                    >
                      <h3 className="font-bold text-gray-900 mb-2">{precedent.title}</h3>
                      <p className="text-sm text-gray-700">{precedent.content}</p>
                      <div className="mt-2 text-xs text-gray-500">
                        Relevance: {(precedent.score * 100).toFixed(0)}%
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            )}
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
                d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"
              />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No mediation yet</h3>
            <p className="text-gray-600">
              Enter dispute details above to get AI-powered mediation suggestions
            </p>
          </Card>
        )}
      </div>
    </div>
  )
}
