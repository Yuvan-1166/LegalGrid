import { useState } from 'react'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorAlert from '../components/ErrorAlert'
import { checkCompliance } from '../services/api'

export default function Compliance() {
  const [orgProfile, setOrgProfile] = useState({
    name: '',
    type: 'private_company',
    industry: 'technology',
    size: '50-200',
    jurisdiction: 'All-India'
  })
  
  const [selectedRegulations, setSelectedRegulations] = useState([])
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const commonRegulations = [
    'Companies Act 2013',
    'Income Tax Act 1961',
    'GST Act 2017',
    'Labour Laws (Minimum Wages Act)',
    'Shops and Establishments Act',
    'EPF and Miscellaneous Provisions Act',
    'Payment of Gratuity Act',
    'Sexual Harassment of Women at Workplace Act',
    'Information Technology Act 2000',
    'Data Protection Regulations'
  ]

  const handleRegulationToggle = (regulation) => {
    setSelectedRegulations(prev =>
      prev.includes(regulation)
        ? prev.filter(r => r !== regulation)
        : [...prev, regulation]
    )
  }

  const handleCheckCompliance = async () => {
    if (!orgProfile.name.trim()) {
      setError('Please enter organization name')
      return
    }

    if (selectedRegulations.length === 0) {
      setError('Please select at least one regulation')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await checkCompliance(orgProfile, selectedRegulations)
      setResult(data.report)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Compliance check failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-green-50/30 to-slate-50">
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-full text-sm font-medium mb-4">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
            </svg>
            Compliance Monitoring
          </div>
          <h1 className="text-4xl font-bold text-slate-900 mb-3 tracking-tight">
            Check compliance status
          </h1>
          <p className="text-lg text-slate-600">
            Monitor your organization's compliance with Indian regulations
          </p>
        </div>

        {/* Organization Profile */}
        <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8 mb-6">
          <h2 className="text-xl font-bold text-slate-900 mb-6">Organization profile</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Organization name
              </label>
              <input
                type="text"
                value={orgProfile.name}
                onChange={(e) => setOrgProfile({ ...orgProfile, name: e.target.value })}
                placeholder="e.g., Tech Innovations Pvt Ltd"
                className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Organization type
              </label>
              <select
                value={orgProfile.type}
                onChange={(e) => setOrgProfile({ ...orgProfile, type: e.target.value })}
                className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent appearance-none bg-white cursor-pointer"
              >
                <option value="private_company">Private Company</option>
                <option value="public_company">Public Company</option>
                <option value="startup">Startup</option>
                <option value="partnership">Partnership</option>
                <option value="sole_proprietorship">Sole Proprietorship</option>
                <option value="llp">LLP</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Industry
              </label>
              <select
                value={orgProfile.industry}
                onChange={(e) => setOrgProfile({ ...orgProfile, industry: e.target.value })}
                className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent appearance-none bg-white cursor-pointer"
              >
                <option value="technology">Technology</option>
                <option value="manufacturing">Manufacturing</option>
                <option value="finance">Finance</option>
                <option value="healthcare">Healthcare</option>
                <option value="retail">Retail</option>
                <option value="education">Education</option>
                <option value="consulting">Consulting</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Company size
              </label>
              <select
                value={orgProfile.size}
                onChange={(e) => setOrgProfile({ ...orgProfile, size: e.target.value })}
                className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent appearance-none bg-white cursor-pointer"
              >
                <option value="1-50">1-50 employees</option>
                <option value="50-200">50-200 employees</option>
                <option value="200-1000">200-1000 employees</option>
                <option value="1000+">1000+ employees</option>
              </select>
            </div>
          </div>
        </div>

        {/* Regulations Selection */}
        <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8 mb-6">
          <h2 className="text-xl font-bold text-slate-900 mb-6">Select regulations</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
            {commonRegulations.map((regulation) => (
              <label
                key={regulation}
                className={`flex items-center p-4 border-2 rounded-xl cursor-pointer transition-all duration-200 ${
                  selectedRegulations.includes(regulation)
                    ? 'border-green-500 bg-green-50'
                    : 'border-slate-200 hover:border-green-300 hover:bg-green-50/50'
                }`}
              >
                <input
                  type="checkbox"
                  checked={selectedRegulations.includes(regulation)}
                  onChange={() => handleRegulationToggle(regulation)}
                  className="w-5 h-5 text-green-600 rounded focus:ring-2 focus:ring-green-500"
                />
                <span className="ml-3 text-sm font-medium text-slate-700">{regulation}</span>
              </label>
            ))}
          </div>

          {selectedRegulations.length > 0 && (
            <div className="mb-6 p-5 bg-green-50 rounded-xl border border-green-200">
              <p className="text-sm font-semibold text-green-800 mb-3">
                {selectedRegulations.length} regulation(s) selected
              </p>
              <div className="flex flex-wrap gap-2">
                {selectedRegulations.map((reg) => (
                  <span
                    key={reg}
                    className="inline-flex items-center px-4 py-2 bg-white border border-green-300 rounded-lg text-sm font-medium text-green-800 shadow-sm"
                  >
                    {reg}
                    <button
                      onClick={() => handleRegulationToggle(reg)}
                      className="ml-2 text-green-600 hover:text-green-800 font-bold"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>
          )}

          <button
            onClick={handleCheckCompliance}
            disabled={loading}
            className="w-full px-6 py-3 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-xl hover:from-green-700 hover:to-green-800 disabled:from-slate-400 disabled:to-slate-400 disabled:cursor-not-allowed font-semibold shadow-lg shadow-green-500/30 hover:shadow-xl hover:shadow-green-500/40 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]"
          >
            {loading ? 'Checking...' : 'Check compliance'}
          </button>
        </div>

        {error && (
          <div className="mb-8">
            <ErrorAlert error={error} onDismiss={() => setError(null)} />
          </div>
        )}

        {loading && (
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl p-16 text-center">
            <LoadingSpinner size="lg" text="Analyzing compliance..." />
          </div>
        )}

        {result && !loading && (
          <div className="space-y-6">
            {/* Compliance Score */}
            <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 overflow-hidden">
              <div className={`h-2 ${
                result.compliance_score >= 80 ? 'bg-gradient-to-r from-emerald-500 to-green-600' :
                result.compliance_score >= 60 ? 'bg-gradient-to-r from-amber-500 to-orange-600' :
                'bg-gradient-to-r from-red-500 to-rose-600'
              }`}></div>
              <div className="p-8">
                <h2 className="text-2xl font-bold text-slate-900 mb-6">Compliance report</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className={`relative overflow-hidden rounded-xl p-6 ${
                    result.compliance_score >= 80 ? 'bg-gradient-to-br from-emerald-500 to-green-600' :
                    result.compliance_score >= 60 ? 'bg-gradient-to-br from-amber-500 to-orange-600' :
                    'bg-gradient-to-br from-red-500 to-rose-600'
                  }`}>
                    <div className="relative z-10">
                      <div className="text-sm font-medium text-white/80 mb-2">Overall score</div>
                      <div className="text-4xl font-bold text-white">
                        {result.compliance_score.toFixed(1)}%
                      </div>
                    </div>
                    <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16"></div>
                  </div>
                  
                  <div className="relative overflow-hidden rounded-xl p-6 bg-gradient-to-br from-blue-500 to-indigo-600">
                    <div className="relative z-10">
                      <div className="text-sm font-medium text-white/80 mb-2">Compliant</div>
                      <div className="text-4xl font-bold text-white">{result.compliant_count}</div>
                    </div>
                    <div className="absolute bottom-0 right-0 w-24 h-24 bg-white/10 rounded-full -mr-12 -mb-12"></div>
                  </div>
                  
                  <div className="relative overflow-hidden rounded-xl p-6 bg-gradient-to-br from-orange-500 to-red-600">
                    <div className="relative z-10">
                      <div className="text-sm font-medium text-white/80 mb-2">Gaps found</div>
                      <div className="text-4xl font-bold text-white">{result.gaps.length}</div>
                    </div>
                    <div className="absolute top-0 left-0 w-20 h-20 bg-white/10 rounded-full -ml-10 -mt-10"></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Compliance Gaps */}
            {result.gaps.length > 0 && (
              <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl shadow-slate-200/50 p-8">
                <h2 className="text-2xl font-bold text-slate-900 mb-6">Compliance gaps</h2>
                <div className="space-y-5">
                  {result.gaps.map((gap, index) => (
                    <div key={index} className="group border border-slate-200 rounded-xl p-6 hover:border-orange-300 hover:shadow-lg transition-all duration-200">
                      <div className="flex justify-between items-start mb-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-3">
                            <span className={`px-4 py-1.5 rounded-full text-xs font-bold ${
                              gap.severity === 'high' ? 'bg-red-100 text-red-700' :
                              gap.severity === 'medium' ? 'bg-amber-100 text-amber-700' :
                              'bg-blue-100 text-blue-700'
                            }`}>
                              {gap.severity.toUpperCase()}
                            </span>
                            <h3 className="text-lg font-bold text-slate-900">{gap.regulation}</h3>
                          </div>
                          <p className="text-slate-700 mb-3 leading-relaxed">{gap.requirement}</p>
                          <div className="text-sm text-slate-600">
                            <span className="font-semibold">Deadline:</span> {gap.deadline}
                          </div>
                        </div>
                      </div>

                      <div className="bg-amber-50 p-5 rounded-xl border-l-4 border-amber-400">
                        <h4 className="text-sm font-semibold text-amber-800 mb-3 flex items-center gap-2">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                          </svg>
                          Action items
                        </h4>
                        <ul className="space-y-2">
                          {gap.action_items.map((action, idx) => (
                            <li key={idx} className="text-sm text-amber-900 flex items-start gap-2">
                              <span className="text-amber-400 mt-1">•</span>
                              <span>{action}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Success Message */}
            {result.gaps.length === 0 && (
              <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-green-200 shadow-xl p-8">
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center flex-shrink-0">
                    <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-slate-900 mb-1">All clear!</h3>
                    <p className="text-slate-600">
                      No compliance gaps detected. Your organization appears to be compliant with all checked regulations.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {!result && !loading && !error && (
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/60 shadow-xl p-16 text-center">
            <div className="w-20 h-20 mx-auto mb-6 bg-green-100 rounded-2xl flex items-center justify-center">
              <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-slate-900 mb-2">Start compliance check</h3>
            <p className="text-slate-600">
              Fill in your organization details and select regulations
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
