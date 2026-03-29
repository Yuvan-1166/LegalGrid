import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import ContractAnalysis from './pages/ContractAnalysis'
import CaseSearch from './pages/CaseSearch'
import Compliance from './pages/Compliance'
import Disputes from './pages/Disputes'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <Link to="/" className="flex items-center">
                  <span className="text-2xl font-bold text-indigo-600">⚖️ LegalGrid</span>
                </Link>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <Link
                    to="/contracts"
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-indigo-600"
                  >
                    Contracts
                  </Link>
                  <Link
                    to="/cases"
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
                  >
                    Case Law
                  </Link>
                  <Link
                    to="/compliance"
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
                  >
                    Compliance
                  </Link>
                  <Link
                    to="/disputes"
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
                  >
                    Disputes
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/contracts" element={<ContractAnalysis />} />
            <Route path="/cases" element={<CaseSearch />} />
            <Route path="/compliance" element={<Compliance />} />
            <Route path="/disputes" element={<Disputes />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
