import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative bg-slate-900 text-white overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900"></div>
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500 rounded-full filter blur-3xl"></div>
          <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500 rounded-full filter blur-3xl"></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-6 py-24 lg:py-32">
          <div className="max-w-3xl">
            <h1 className="text-5xl lg:text-6xl font-bold leading-tight mb-6">
              Legal intelligence for modern practice
            </h1>
            <p className="text-xl text-slate-300 mb-8 leading-relaxed">
              Analyze contracts, research case law, monitor compliance, and resolve disputes with intelligent tools built for Indian legal professionals.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link
                to="/contracts"
                className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition"
              >
                Start free trial
              </Link>
              <Link
                to="/cases"
                className="px-8 py-4 bg-white/10 hover:bg-white/20 text-white font-semibold rounded-lg border border-white/20 transition"
              >
                See how it works
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Bar */}
      <section className="border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-slate-900 mb-1">95%</div>
              <div className="text-sm text-slate-600">Analysis accuracy</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-slate-900 mb-1">&lt;3s</div>
              <div className="text-sm text-slate-600">Average response time</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-slate-900 mb-1">24/7</div>
              <div className="text-sm text-slate-600">Always available</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-slate-900 mb-1">100%</div>
              <div className="text-sm text-slate-600">Data security</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-slate-50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-slate-900 mb-4">
              Everything you need in one platform
            </h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Comprehensive tools designed for the complete legal workflow
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-8">
            <Link to="/contracts" className="group bg-white p-8 rounded-xl border border-slate-200 hover:border-blue-500 hover:shadow-lg transition">
              <div className="flex items-start gap-4 mb-4">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center text-2xl flex-shrink-0">
                  📄
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900 mb-2">Contract Analysis</h3>
                  <p className="text-slate-600 leading-relaxed">
                    Review contracts for risks, compliance issues, and unfavorable terms. Get detailed clause-by-clause analysis with actionable recommendations.
                  </p>
                </div>
              </div>
              <div className="text-blue-600 font-semibold group-hover:translate-x-1 transition-transform inline-block">
                Learn more →
              </div>
            </Link>

            <Link to="/cases" className="group bg-white p-8 rounded-xl border border-slate-200 hover:border-blue-500 hover:shadow-lg transition">
              <div className="flex items-start gap-4 mb-4">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center text-2xl flex-shrink-0">
                  ⚖️
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900 mb-2">Case Law Research</h3>
                  <p className="text-slate-600 leading-relaxed">
                    Search Supreme Court and High Court judgments with intelligent semantic search. Find relevant precedents faster with context-aware results.
                  </p>
                </div>
              </div>
              <div className="text-blue-600 font-semibold group-hover:translate-x-1 transition-transform inline-block">
                Learn more →
              </div>
            </Link>

            <Link to="/compliance" className="group bg-white p-8 rounded-xl border border-slate-200 hover:border-blue-500 hover:shadow-lg transition">
              <div className="flex items-start gap-4 mb-4">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center text-2xl flex-shrink-0">
                  ✅
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900 mb-2">Compliance Monitoring</h3>
                  <p className="text-slate-600 leading-relaxed">
                    Track regulatory compliance across multiple frameworks. Identify gaps and receive recommendations to maintain full compliance.
                  </p>
                </div>
              </div>
              <div className="text-blue-600 font-semibold group-hover:translate-x-1 transition-transform inline-block">
                Learn more →
              </div>
            </Link>

            <Link to="/disputes" className="group bg-white p-8 rounded-xl border border-slate-200 hover:border-blue-500 hover:shadow-lg transition">
              <div className="flex items-start gap-4 mb-4">
                <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center text-2xl flex-shrink-0">
                  🤝
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900 mb-2">Dispute Resolution</h3>
                  <p className="text-slate-600 leading-relaxed">
                    Facilitate multi-party dispute mediation with fair outcome generation. Get comprehensive resolution strategies and settlement options.
                  </p>
                </div>
              </div>
              <div className="text-blue-600 font-semibold group-hover:translate-x-1 transition-transform inline-block">
                Learn more →
              </div>
            </Link>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-slate-900 mb-4">
              Built for legal professionals
            </h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Designed to integrate seamlessly into your existing workflow
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-12">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center text-2xl mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Input your query</h3>
              <p className="text-slate-600">
                Upload documents, enter search terms, or describe your legal question in plain language.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center text-2xl mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Get instant analysis</h3>
              <p className="text-slate-600">
                Our system processes your request using advanced legal intelligence trained on Indian law.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center text-2xl mx-auto mb-4">
                3
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Take action</h3>
              <p className="text-slate-600">
                Review detailed insights, export reports, and make informed decisions with confidence.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-slate-900 text-white">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold mb-4">
            Ready to get started?
          </h2>
          <p className="text-xl text-slate-300 mb-8">
            Start using intelligent legal tools today. No credit card required.
          </p>
          <Link
            to="/contracts"
            className="inline-block px-10 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition"
          >
            Try it free
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-6 text-center text-slate-600 text-sm">
          © 2026 Smart Legal System. All rights reserved.
        </div>
      </footer>
    </div>
  )
}

