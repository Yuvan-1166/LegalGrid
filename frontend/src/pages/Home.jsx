import { Link } from 'react-router-dom'
import Badge from '../components/Badge'
import Tooltip from '../components/Tooltip'

export default function Home() {
  const features = [
    {
      title: 'Contract Analysis',
      description: 'Analyze contracts for risks, red flags, and compliance with Indian law',
      icon: '📄',
      link: '/contracts',
      color: 'bg-gradient-to-br from-blue-50 to-blue-100 hover:from-blue-100 hover:to-blue-200',
      badge: 'AI-Powered',
      stats: '95% Accuracy'
    },
    {
      title: 'Case Law Search',
      description: 'Find relevant precedents from Supreme Court and High Courts',
      icon: '⚖️',
      link: '/cases',
      color: 'bg-gradient-to-br from-purple-50 to-purple-100 hover:from-purple-100 hover:to-purple-200',
      badge: 'Hybrid Search',
      stats: '20+ Cases'
    },
    {
      title: 'Compliance Check',
      description: 'Monitor regulatory compliance and detect gaps',
      icon: '✅',
      link: '/compliance',
      color: 'bg-gradient-to-br from-green-50 to-green-100 hover:from-green-100 hover:to-green-200',
      badge: 'Real-time',
      stats: 'Multi-Regulation'
    },
    {
      title: 'Dispute Mediation',
      description: 'AI-powered multi-party dispute resolution',
      icon: '🤝',
      link: '/disputes',
      color: 'bg-gradient-to-br from-orange-50 to-orange-100 hover:from-orange-100 hover:to-orange-200',
      badge: 'Fair Outcomes',
      stats: 'Multi-Party'
    },
  ]

  const stats = [
    { label: 'Documents Indexed', value: '20+', icon: '📚' },
    { label: 'API Endpoints', value: '13', icon: '🔌' },
    { label: 'Response Time', value: '<3s', icon: '⚡' },
    { label: 'Accuracy', value: '95%', icon: '🎯' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16 animate-fade-in">
          <Badge variant="info" size="lg">
            🚀 Powered by RAG & Hybrid Search
          </Badge>
          <h1 className="text-6xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-4 mt-6">
            Smart Legal System
          </h1>
          <p className="text-2xl text-gray-600 mb-4">
            AI-powered legal analysis for Indian law
          </p>
          <p className="text-lg text-gray-500 mb-8 max-w-2xl mx-auto">
            Combining semantic search, BM25 ranking, and GROQ LLM for accurate legal research and analysis
          </p>
          <div className="flex justify-center gap-4">
            <Link
              to="/contracts"
              className="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:from-indigo-700 hover:to-purple-700 transition transform hover:scale-105 shadow-lg font-semibold"
            >
              Get Started →
            </Link>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 bg-white text-indigo-600 border-2 border-indigo-600 rounded-xl hover:bg-indigo-50 transition transform hover:scale-105 shadow-lg font-semibold"
            >
              API Docs 📖
            </a>
          </div>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
          {stats.map((stat) => (
            <div key={stat.label} className="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition text-center">
              <div className="text-3xl mb-2">{stat.icon}</div>
              <div className="text-3xl font-bold text-indigo-600 mb-1">{stat.value}</div>
              <div className="text-sm text-gray-600">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Features Grid */}
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-8">
          Explore Features
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16">
          {features.map((feature) => (
            <Link
              key={feature.title}
              to={feature.link}
              className={`${feature.color} p-8 rounded-2xl border-2 border-transparent hover:border-indigo-400 transition transform hover:scale-105 shadow-md hover:shadow-xl`}
            >
              <div className="flex justify-between items-start mb-4">
                <div className="text-5xl">{feature.icon}</div>
                <Badge variant="purple">{feature.badge}</Badge>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-700 mb-4">{feature.description}</p>
              <div className="flex items-center text-sm text-gray-600">
                <span className="font-semibold">{feature.stats}</span>
                <span className="ml-auto text-indigo-600 font-semibold">Explore →</span>
              </div>
            </Link>
          ))}
        </div>

        {/* Tech Stack */}
        <div className="bg-white rounded-2xl p-8 shadow-lg">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-6">
            Built With Modern Tech
          </h2>
          <div className="flex flex-wrap justify-center gap-4">
            {[
              { name: 'FastAPI', desc: 'High-performance backend' },
              { name: 'React 19', desc: 'Modern UI framework' },
              { name: 'Qdrant', desc: 'Vector database' },
              { name: 'GROQ', desc: 'Fast LLM inference' },
              { name: 'LangChain', desc: 'Agent framework' },
              { name: 'TailwindCSS', desc: 'Utility-first CSS' }
            ].map((tech) => (
              <Tooltip key={tech.name} content={tech.desc} position="top">
                <span className="px-6 py-3 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl text-sm font-semibold text-gray-800 border border-gray-200 hover:border-indigo-300 transition cursor-pointer">
                  {tech.name}
                </span>
              </Tooltip>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center text-gray-500 text-sm">
          <p>© 2026 LegalGrid Smart Legal System • Built with ❤️ for Indian Law</p>
        </div>
      </div>
    </div>
  )
}

