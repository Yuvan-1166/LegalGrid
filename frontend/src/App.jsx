import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import Home from './pages/Home'
import ContractAnalysis from './pages/ContractAnalysis'
import CaseSearch from './pages/CaseSearch'
import Compliance from './pages/Compliance'
import Disputes from './pages/Disputes'
import Chat from './pages/Chat'

function Navigation() {
  const location = useLocation()
  
  const isActive = (path) => {
    return location.pathname === path
  }

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-12">
            <Link to="/" className="flex items-center gap-2">
              <svg className="w-7 h-7 text-slate-900" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L3 7v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5zm0 10h7c-.53 4.12-3.28 7.79-7 8.94V12H5V7.3l7-3.89v8.59z"/>
              </svg>
              <span className="text-xl font-bold text-slate-900">LegalGrid</span>
            </Link>
            
            <div className="hidden md:flex items-center gap-1">
              <Link
                to="/contracts"
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  isActive('/contracts')
                    ? 'bg-slate-100 text-slate-900'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                Contracts
              </Link>
              <Link
                to="/cases"
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  isActive('/cases')
                    ? 'bg-slate-100 text-slate-900'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                Case Law
              </Link>
              <Link
                to="/compliance"
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  isActive('/compliance')
                    ? 'bg-slate-100 text-slate-900'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                Compliance
              </Link>
              <Link
                to="/disputes"
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  isActive('/disputes')
                    ? 'bg-slate-100 text-slate-900'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                Disputes
              </Link>
              <Link
                to="/chat"
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  isActive('/chat')
                    ? 'bg-slate-100 text-slate-900'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                AI Chat
              </Link>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <Link
              to="/contracts"
              className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-lg transition"
            >
              Get started
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  )
}

function AppContent() {
  const location = useLocation()
  const isChatPage = location.pathname === '/chat'
  
  return (
    <div className="h-screen flex flex-col bg-white overflow-hidden">
      <Navigation />
      <main className={isChatPage ? 'flex-1 overflow-hidden' : 'flex-1 overflow-y-auto'}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/contracts" element={<ContractAnalysis />} />
          <Route path="/cases" element={<CaseSearch />} />
          <Route path="/compliance" element={<Compliance />} />
          <Route path="/disputes" element={<Disputes />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
