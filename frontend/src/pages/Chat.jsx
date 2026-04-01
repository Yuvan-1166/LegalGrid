import { useState, useRef, useEffect } from 'react'
import { 
  chatWithAI, 
  uploadChatDocument, 
  listChatSessions, 
  createChatSession, 
  getChatSession, 
  deleteChatSession,
  updateSessionTitle 
} from '../services/api'

export default function Chat() {
  const [sessions, setSessions] = useState([])
  const [currentSessionId, setCurrentSessionId] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [uploadedFile, setUploadedFile] = useState(null)
  const [showTemplates, setShowTemplates] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [editingSessionId, setEditingSessionId] = useState(null)
  const [editingTitle, setEditingTitle] = useState('')
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)
  const templatesRef = useRef(null)

  const templates = [
    { id: 1, label: 'Contract Review', prompt: 'I need help reviewing a contract for potential risks and compliance issues.' },
    { id: 2, label: 'Case Law Research', prompt: 'I\'m looking for legal precedents related to ' },
    { id: 3, label: 'Compliance Guidance', prompt: 'What are the compliance requirements under ' },
    { id: 4, label: 'Dispute Mediation', prompt: 'I need assistance with mediating a dispute regarding ' },
    { id: 5, label: 'Legal Interpretation', prompt: 'Can you help me understand the legal implications of ' },
    { id: 6, label: 'Document Drafting', prompt: 'I need guidance on drafting a legal document for ' },
  ]

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    loadSessions()
  }, [])

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (templatesRef.current && !templatesRef.current.contains(event.target)) {
        setShowTemplates(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const loadSessions = async () => {
    try {
      const data = await listChatSessions()
      setSessions(data.sessions || [])
    } catch (error) {
      console.error('Failed to load sessions:', error)
    }
  }

  const loadSession = async (sessionId) => {
    try {
      const session = await getChatSession(sessionId)
      setCurrentSessionId(session.session_id)
      
      const formattedMessages = session.messages.map(msg => ({
        id: msg.id,
        type: msg.role === 'user' ? 'user' : 'assistant',
        content: msg.content,
        timestamp: new Date(msg.timestamp),
      }))
      
      setMessages(formattedMessages)
    } catch (error) {
      console.error('Failed to load session:', error)
    }
  }

  const handleNewChat = async () => {
    try {
      const data = await createChatSession()
      setCurrentSessionId(data.session_id)
      setMessages([])
      await loadSessions()
    } catch (error) {
      console.error('Failed to create session:', error)
    }
  }

  const handleDeleteSession = async (sessionId, e) => {
    e.stopPropagation()
    if (!confirm('Delete this conversation?')) return
    
    try {
      await deleteChatSession(sessionId)
      await loadSessions()
      
      if (currentSessionId === sessionId) {
        handleNewChat()
      }
    } catch (error) {
      console.error('Failed to delete session:', error)
    }
  }

  const handleEditTitle = async (sessionId, newTitle) => {
    try {
      await updateSessionTitle(sessionId, newTitle)
      await loadSessions()
      setEditingSessionId(null)
      setEditingTitle('')
    } catch (error) {
      console.error('Failed to update title:', error)
    }
  }

  const handleSend = async () => {
    if (!input.trim() && !uploadedFile) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
      file: uploadedFile,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      let response
      if (uploadedFile) {
        response = await uploadChatDocument(uploadedFile, input, currentSessionId)
      } else {
        response = await chatWithAI(input, currentSessionId)
      }

      if (response.session_id && !currentSessionId) {
        setCurrentSessionId(response.session_id)
        await loadSessions()
      }

      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.message,
        suggestions: response.suggestions,
        timestamp: new Date(),
      }

      setMessages(prev => [...prev, assistantMessage])
      setUploadedFile(null)
    } catch (err) {
      console.error('Chat error:', err)
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'I apologize, but I encountered an error. Please try again.',
        error: true,
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleTemplateSelect = (template) => {
    setInput(template.prompt)
    setShowTemplates(false)
  }

  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      setUploadedFile(file)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const exportChat = () => {
    const chatText = messages.map(m => 
      `[${m.timestamp.toLocaleTimeString()}] ${m.type === 'user' ? 'You' : 'Assistant'}: ${m.content}`
    ).join('\n\n')
    
    const blob = new Blob([chatText], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `legal-chat-${new Date().toISOString().split('T')[0]}.txt`
    a.click()
  }

  return (
    <div className="flex h-full bg-white">
      {/* Sidebar - ChatGPT Style with Your Color Scheme */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 bg-slate-50 border-r border-slate-200 flex flex-col overflow-hidden flex-shrink-0`}>
        {/* Sidebar Header */}
        <div className="p-3 border-b border-slate-200">
          <button
            onClick={handleNewChat}
            className="w-full px-3 py-2.5 border border-slate-300 hover:bg-slate-100 hover:border-slate-400 text-slate-700 rounded-lg text-sm font-medium transition-all cursor-pointer flex items-center justify-center gap-2 shadow-sm"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New chat
          </button>
        </div>

        {/* Sessions List */}
        <div className="flex-1 overflow-y-auto p-2">
          {sessions.length === 0 ? (
            <div className="px-3 py-8 text-center text-sm text-slate-500">
              No conversations yet
            </div>
          ) : (
            sessions.map((session) => (
              <div
                key={session.session_id}
                className={`group relative px-3 py-2.5 mb-1 rounded-lg cursor-pointer transition-colors ${
                  currentSessionId === session.session_id
                    ? 'bg-slate-200'
                    : 'hover:bg-slate-100'
                }`}
                onClick={() => loadSession(session.session_id)}
              >
                <div className="flex items-center justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    {editingSessionId === session.session_id ? (
                      <input
                        type="text"
                        value={editingTitle}
                        onChange={(e) => setEditingTitle(e.target.value)}
                        onBlur={() => handleEditTitle(session.session_id, editingTitle)}
                        onKeyPress={(e) => {
                          if (e.key === 'Enter') {
                            handleEditTitle(session.session_id, editingTitle)
                          }
                        }}
                        onClick={(e) => e.stopPropagation()}
                        className="w-full px-2 py-1 text-sm bg-white text-slate-900 border border-blue-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                        autoFocus
                      />
                    ) : (
                      <div className="flex items-center gap-2">
                        <svg className="w-4 h-4 text-slate-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                        </svg>
                        <p className="text-sm text-slate-700 truncate">{session.title}</p>
                      </div>
                    )}
                  </div>
                  <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        setEditingSessionId(session.session_id)
                        setEditingTitle(session.title)
                      }}
                      className="p-1 text-slate-500 hover:text-slate-900 transition-colors cursor-pointer"
                      title="Rename"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button
                      onClick={(e) => handleDeleteSession(session.session_id, e)}
                      className="p-1 text-slate-500 hover:text-red-600 transition-colors cursor-pointer"
                      title="Delete"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Sidebar Footer */}
        <div className="p-3 border-t border-slate-200">
          <button
            onClick={exportChat}
            className="w-full px-3 py-2 text-sm text-slate-700 hover:bg-slate-100 rounded-lg transition-all cursor-pointer flex items-center gap-2 hover:shadow-sm"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Export chat
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Bar */}
        <div className="h-14 border-b border-slate-200 flex items-center justify-between px-4 bg-white flex-shrink-0">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-slate-100 rounded-lg transition-all cursor-pointer hover:shadow-sm"
            >
              <svg className="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <h1 className="text-sm font-semibold text-slate-900">
              {currentSessionId ? sessions.find(s => s.session_id === currentSessionId)?.title || 'Legal Assistant' : 'Legal Assistant'}
            </h1>
          </div>
          <button
            onClick={handleNewChat}
            className="p-2 hover:bg-slate-100 rounded-lg transition-all cursor-pointer hover:shadow-sm"
            title="New chat"
          >
            <svg className="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto">
          {messages.length === 0 ? (
            /* Empty State - ChatGPT Style */
            <div className="h-full flex flex-col items-center justify-center px-4 pb-32">
              <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mb-6">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                </svg>
              </div>
              <h2 className="text-2xl font-semibold text-slate-900 mb-3">How can I help you today?</h2>
              <p className="text-sm text-slate-600 mb-8 text-center max-w-md">
                I'm your legal assistant specializing in Indian law. Ask me about contracts, case law, compliance, or disputes.
              </p>
              
              {/* Quick Start Cards */}
              <div className="grid grid-cols-2 gap-3 max-w-2xl w-full">
                {templates.slice(0, 4).map((template) => (
                  <button
                    key={template.id}
                    onClick={() => handleTemplateSelect(template)}
                    className="p-4 bg-white hover:bg-slate-50 border border-slate-200 hover:border-slate-300 rounded-xl text-left transition-all cursor-pointer shadow-sm hover:shadow-md"
                  >
                    <p className="text-sm font-medium text-slate-900 mb-1">{template.label}</p>
                    <p className="text-xs text-slate-600 line-clamp-2">{template.prompt}</p>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            /* Messages */
            <div className="max-w-3xl mx-auto px-4 py-6">
              {messages.map((message) => (
                <div key={message.id} className="mb-8">
                  <div className={`flex gap-4 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                    {message.type === 'assistant' && (
                      <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0">
                        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                        </svg>
                      </div>
                    )}
                    
                    <div className="flex-1 max-w-3xl">
                      <div className={`${message.type === 'user' ? 'bg-slate-100' : ''} ${message.type === 'user' ? 'rounded-2xl px-4 py-3' : ''}`}>
                        <p className={`text-[15px] leading-7 ${message.type === 'user' ? 'text-slate-900' : 'text-slate-800'} whitespace-pre-wrap`}>
                          {message.content}
                        </p>
                        {message.file && (
                          <div className="mt-2 pt-2 border-t border-slate-200 flex items-center gap-2 text-xs text-slate-600">
                            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M8 4a3 3 0 00-3 3v4a5 5 0 0010 0V7a1 1 0 112 0v4a7 7 0 11-14 0V7a5 5 0 0110 0v4a3 3 0 11-6 0V7a1 1 0 012 0v4a1 1 0 102 0V7a3 3 0 00-3-3z" clipRule="evenodd" />
                            </svg>
                            {message.file.name}
                          </div>
                        )}
                      </div>

                      {/* Suggestions */}
                      {message.suggestions && message.suggestions.length > 0 && message.type === 'assistant' && (
                        <div className="mt-4 space-y-2">
                          {message.suggestions.map((suggestion, idx) => (
                            <button
                              key={idx}
                              onClick={() => setInput(suggestion)}
                              className="block w-full text-left px-4 py-2.5 bg-white border border-slate-200 hover:border-slate-300 rounded-xl hover:bg-slate-50 text-sm text-slate-700 transition-all cursor-pointer shadow-sm hover:shadow"
                            >
                              {suggestion}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>

                    {message.type === 'user' && (
                      <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center flex-shrink-0">
                        <span className="text-white text-xs font-semibold">Y</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {/* Typing Indicator */}
              {loading && (
                <div className="mb-8">
                  <div className="flex gap-4">
                    <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0">
                      <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                      </svg>
                    </div>
                    <div className="flex items-center">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area - Fixed at Bottom */}
        <div className="border-t border-slate-200 bg-white p-4 flex-shrink-0">
          <div className="max-w-3xl mx-auto">
            {uploadedFile && (
              <div className="mb-3 flex items-center gap-2 px-3 py-2 bg-blue-50 border border-blue-200 rounded-lg">
                <svg className="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8 4a3 3 0 00-3 3v4a5 5 0 0010 0V7a1 1 0 112 0v4a7 7 0 11-14 0V7a5 5 0 0110 0v4a3 3 0 11-6 0V7a1 1 0 012 0v4a1 1 0 102 0V7a3 3 0 00-3-3z" clipRule="evenodd" />
                </svg>
                <span className="text-sm text-blue-900 flex-1">{uploadedFile.name}</span>
                <button
                  onClick={() => setUploadedFile(null)}
                  className="text-blue-600 hover:text-blue-800 cursor-pointer"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            )}
            
            <div className="relative bg-white border border-slate-300 rounded-2xl shadow-sm hover:shadow-md focus-within:border-slate-400 focus-within:shadow-md transition-all">
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileUpload}
                accept=".pdf,.txt,.doc,.docx"
                className="hidden"
              />
              
              <div className="flex items-end gap-2 p-2">
                {/* Templates Button */}
                <div className="relative" ref={templatesRef}>
                  <button
                    onClick={() => setShowTemplates(!showTemplates)}
                    className="p-2 hover:bg-slate-100 rounded-lg transition-all cursor-pointer hover:shadow-sm"
                    title="Templates"
                  >
                    <svg className="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                  </button>
                  
                  {showTemplates && (
                    <div className="absolute bottom-full left-0 mb-2 w-80 bg-white border border-slate-200 rounded-xl shadow-xl overflow-hidden z-50">
                      <div className="px-4 py-3 bg-slate-50 border-b border-slate-200">
                        <p className="text-sm font-semibold text-slate-900">Quick Templates</p>
                      </div>
                      <div className="max-h-96 overflow-y-auto">
                        {templates.map((template) => (
                          <button
                            key={template.id}
                            onClick={() => handleTemplateSelect(template)}
                            className="w-full text-left px-4 py-3 hover:bg-slate-50 transition-all cursor-pointer border-b border-slate-100 last:border-b-0"
                          >
                            <p className="text-sm font-medium text-slate-900">{template.label}</p>
                            <p className="text-xs text-slate-500 mt-1 line-clamp-2">{template.prompt}</p>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* File Upload Button */}
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="p-2 hover:bg-slate-100 rounded-lg transition-all cursor-pointer hover:shadow-sm"
                  title="Attach file"
                >
                  <svg className="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                  </svg>
                </button>

                {/* Text Input */}
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Message Legal Assistant"
                  className="flex-1 px-3 py-2 bg-transparent focus:outline-none resize-none text-[15px] text-slate-900 placeholder-slate-400 max-h-52"
                  rows="1"
                  style={{ 
                    minHeight: '24px',
                    height: 'auto',
                  }}
                  onInput={(e) => {
                    e.target.style.height = 'auto'
                    e.target.style.height = e.target.scrollHeight + 'px'
                  }}
                />

                {/* Send Button */}
                <button
                  onClick={handleSend}
                  disabled={loading || (!input.trim() && !uploadedFile)}
                  className="p-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-200 disabled:cursor-not-allowed rounded-lg transition-all cursor-pointer shadow-sm hover:shadow-md active:scale-95"
                  title="Send message"
                >
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
                  </svg>
                </button>
              </div>
            </div>
            
            {/* Footer Text */}
            <p className="text-xs text-center text-slate-500 mt-3">
              Legal Assistant can make mistakes. Verify important information.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
