import { Link } from 'react-router-dom'

export default function Home() {
  const features = [
    {
      title: 'Contract Analysis',
      description: 'Analyze contracts for risks, red flags, and compliance with Indian law',
      icon: '📄',
      link: '/contracts',
      color: 'bg-blue-50 hover:bg-blue-100',
    },
    {
      title: 'Case Law Search',
      description: 'Find relevant precedents from Supreme Court and High Courts',
      icon: '⚖️',
      link: '/cases',
      color: 'bg-purple-50 hover:bg-purple-100',
    },
    {
      title: 'Compliance Check',
      description: 'Monitor regulatory compliance and detect gaps',
      icon: '✅',
      link: '/compliance',
      color: 'bg-green-50 hover:bg-green-100',
    },
    {
      title: 'Dispute Mediation',
      description: 'AI-powered multi-party dispute resolution',
      icon: '🤝',
      link: '/disputes',
      color: 'bg-orange-50 hover:bg-orange-100',
    },
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Smart Legal System
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          RAG-powered legal AI for Indian law analysis
        </p>
        <div className="flex justify-center gap-4">
          <Link
            to="/contracts"
            className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
          >
            Get Started
          </Link>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 bg-white text-indigo-600 border-2 border-indigo-600 rounded-lg hover:bg-indigo-50 transition"
          >
            API Docs
          </a>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {features.map((feature) => (
          <Link
            key={feature.title}
            to={feature.link}
            className={`${feature.color} p-6 rounded-lg border-2 border-transparent hover:border-indigo-300 transition`}
          >
            <div className="text-4xl mb-3">{feature.icon}</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              {feature.title}
            </h3>
            <p className="text-gray-600">{feature.description}</p>
          </Link>
        ))}
      </div>

      {/* Tech Stack */}
      <div className="mt-16 text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Built With</h2>
        <div className="flex flex-wrap justify-center gap-4">
          {['FastAPI', 'React', 'Qdrant', 'GROQ', 'LangChain', 'TailwindCSS'].map((tech) => (
            <span
              key={tech}
              className="px-4 py-2 bg-white rounded-full text-sm font-medium text-gray-700 border border-gray-200"
            >
              {tech}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
