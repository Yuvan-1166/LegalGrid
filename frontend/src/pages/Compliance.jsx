import { useState } from 'react'
import Card from '../components/Card'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorAlert from '../components/ErrorAlert'
import SuccessAlert from '../components/SuccessAlert'
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
  const [customRegulation, setCustomRegulation] = useState('')
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

  const handleAddCustomRegulation = () => {
    if (customRegulation.trim() && !selectedRegulations.includes(customRegulation.trim())) {
      setSelectedRegulations(prev => [...prev, customRegulation.trim()])
      setCustomRegulation('')
    }
  }

  const handleCheckCompliance = async () => {
    if (!orgProfile.name.trim()) {
      setError('Please enter organization name')
      return
    }

    if (selectedRegulations.length === 0) {
      setError('Please select at least one regulation to check')
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

  const getSeverityColor = (severity) => {
    if (severity === 'high') return 'bg-red-100 text-red-800 border-red-300'
    if (severity === 'medium') return 'bg-yellow-100 text-yellow-800 border-yellow-300'
    return 'bg-blue-100 text-blue-800 border-blue-300'
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-teal-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Compliance Monitoring</h1>
          <p className="text-lg text-gray-600">
            Check your organization's compliance with Indian regulations
          </p>
        </div>

        {/* Organization Profile */}
        <Card className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Organization Profile</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Organization Name
              </label>
              <input
                type="text"
                value={orgProfile.name}
                onChange={(e) => setOrgProfile({ ...orgProfile, name: e.target.value })}
                placeholder="e.g., Tech Innovations Pvt Ltd"
                className="w-full px-4 py-2 text-gray-900 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Organization Type
              </label>
              <select
                value={orgProfile.type}
                onChange={(e) => setOrgProfile({ ...orgProfile, type: e.target.value })}
                className="w-full px-4 py-2 text-gray-900 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
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
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Industry
              </label>
              <select
                value={orgProfile.industry}
                onChange={(e) => setOrgProfile({ ...orgProfile, industry: e.target.value })}
                className="w-full px-4 py-2 text-gray-900 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
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
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Company Size
              </label>
              <select
                value={orgProfile.size}
                onChange={(e) => setOrgProfile({ ...orgProfile, size: e.target.value })}
                className="w-full px-4 py-2 text-gray-900 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              >
                <option value="1-50">1-50 employees</option>
                <option value="50-200">50-200 employees</option>
                <option value="200-1000">200-1000 employees</option>
                <option value="1000+">1000+ employees</option>
              </select>
            </div>
          </div>
        </Card>

        {/* Regulations Selection */}
        <Card className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Select Regulations to Check</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
            {commonRegulations.map((regulation) => (
              <label
                key={regulation}
                className="flex items-center p-3 border-2 border-gray-200 rounded-lg hover:border-green-300 cursor-pointer transition-all"
              >
                <input
                  type="checkbox"
                  checked={selectedRegulations.includes(regulation)}
                  onChange={() => handleRegulationToggle(regulation)}
                  className="w-5 h-5 text-green-600 rounded focus:ring-2 focus:ring-green-500"
                />
                <span className="ml-3 text-gray-800">{regulation}</span>
              </label>
            ))}
          </div>

          <div className="flex gap-2">
            <input
              type="text"
              value={customRegulation}
              onChange={(e) => setCustomRegulation(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAddCustomRegulation()}
              placeholder="Add custom regulation..."
              className="flex-1 px-4 py-2 text-gray-900 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
            <button
              onClick={handleAddCustomRegulation}
              className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium"
            >
              Add
            </button>
          </div>

          {selectedRegulations.length > 0 && (
            <div className="mt-4 p-3 bg-green-50 rounded-lg">
              <p className="text-sm font-medium text-green-800 mb-2">
                Selected: {selectedRegulations.length} regulation(s)
              </p>
              <div className="flex flex-wrap gap-2">
                {selectedRegulations.map((reg) => (
                  <span
                    key={reg}
                    className="inline-flex items-center px-3 py-1 bg-white border border-green-300 rounded-full text-sm text-green-800"
                  >
                    {reg}
                    <button
                      onClick={() => handleRegulationToggle(reg)}
                      className="ml-2 text-green-600 hover:text-green-800"
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
            className="w-full mt-4 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium shadow-md hover:shadow-lg transition-all"
          >
            {loading ? 'Checking Compliance...' : '✓ Check Compliance'}
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
            <LoadingSpinner size="lg" text="Analyzing compliance status..." />
          </Card>
        )}

        {/* Results Display */}
        {result && !loading && (
          <div className="space-y-6 animate-fade-in">
            {/* Compliance Score */}
            <Card>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Compliance Report</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-6 bg-gradient-to-br from-green-50 to-teal-50 rounded-lg border-2 border-green-200">
                  <div className="text-sm font-medium text-gray-600 mb-2">Overall Score</div>
                  <div className={`text-4xl font-bold ${getScoreColor(result.compliance_score)}`}>
                    {result.compliance_score.toFixed(1)}%
                  </div>
                </div>
                <div className="p-6 bg-blue-50 rounded-lg border-2 border-blue-200">
                  <div className="text-sm font-medium text-gray-600 mb-2">Compliant</div>
                  <div className="text-4xl font-bold text-blue-600">{result.compliant_count}</div>
                </div>
                <div className="p-6 bg-red-50 rounded-lg border-2 border-red-200">
                  <div className="text-sm font-medium text-gray-600 mb-2">Gaps Found</div>
                  <div className="text-4xl font-bold text-red-600">{result.gaps.length}</div>
                </div>
              </div>
            </Card>

            {/* Compliance Gaps */}
            {result.gaps.length > 0 && (
              <Card>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Compliance Gaps</h2>
                <div className="space-y-4">
                  {result.gaps.map((gap, index) => (
                    <div
                      key={index}
                      className="border-2 border-gray-200 rounded-lg p-5 hover:border-green-300 hover:shadow-md transition-all"
                    >
                      <div className="flex justify-between items-start mb-3">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span className={`px-3 py-1 rounded-full text-xs font-bold border-2 ${getSeverityColor(gap.severity)}`}>
                              {gap.severity.toUpperCase()}
                            </span>
                            <h3 className="text-lg font-bold text-gray-900">{gap.regulation}</h3>
                          </div>
                          <p className="text-gray-700 mb-2">{gap.requirement}</p>
                          <div className="text-sm text-gray-600">
                            <span className="font-medium">Deadline:</span> {gap.deadline}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-xs text-gray-500 mb-1">Confidence</div>
                          <div className="text-lg font-bold text-gray-700">
                            {(gap.confidence * 100).toFixed(0)}%
                          </div>
                        </div>
                      </div>

                      <div className="bg-yellow-50 p-4 rounded border-l-4 border-yellow-400">
                        <h4 className="text-sm font-semibold text-yellow-800 mb-2">Action Items</h4>
                        <ul className="list-disc list-inside space-y-1">
                          {gap.action_items.map((action, idx) => (
                            <li key={idx} className="text-sm text-yellow-900">{action}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            )}

            {/* Success Message */}
            {result.gaps.length === 0 && (
              <SuccessAlert
                message="Congratulations! No compliance gaps detected. Your organization appears to be compliant with all checked regulations."
              />
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
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No compliance check yet</h3>
            <p className="text-gray-600">
              Fill in your organization details and select regulations to check compliance
            </p>
          </Card>
        )}
      </div>
    </div>
  )
}
