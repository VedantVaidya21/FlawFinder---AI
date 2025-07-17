import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { motion } from 'framer-motion'
import { ThemeProvider } from './contexts/ThemeContext'
import Landing from './pages/Landing'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import FixPlan from './pages/FixPlan'
import CEOReport from './pages/CEOReport'
import Navigation from './components/Navigation'
import { useState, useEffect } from 'react'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check authentication status
    const token = localStorage.getItem('authToken')
    if (token) {
      setIsAuthenticated(true)
    }
    setLoading(false)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-zinc-900 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <div className="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-zinc-1000 text-lg">Loading FlawFinder AI...</p>
        </motion.div>
      </div>
    )
  }

  return (
    <ThemeProvider>
      <Router>
        <div className="min-h-screen">
          <Toaster
            position="top-right"
            toastOptions={{
              className: 'glass-dark text-zinc-100',
              style: {
                background: 'rgba(39, 39, 42, 0.8)',
                color: '#fafafa',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(63, 63, 70, 0.3)',
              },
            }}
          />
          
          {isAuthenticated && <Navigation />}
          
          <Routes>
            {/* Public routes */}
            <Route 
              path="/" 
              element={isAuthenticated ? <Dashboard /> : <Landing />} 
            />
            <Route 
              path="/login" 
              element={<Login setIsAuthenticated={setIsAuthenticated} />} 
            />
            <Route 
              path="/signup" 
              element={<Signup setIsAuthenticated={setIsAuthenticated} />} 
            />
            
            {/* Protected routes */}
            <Route 
              path="/dashboard" 
              element={isAuthenticated ? <Dashboard /> : <Landing />} 
            />
            <Route 
              path="/upload" 
              element={isAuthenticated ? <Upload /> : <Landing />} 
            />
            <Route 
              path="/fix-plan" 
              element={isAuthenticated ? <FixPlan /> : <Landing />} 
            />
            <Route 
              path="/ceo-report" 
              element={isAuthenticated ? <CEOReport /> : <Landing />} 
            />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  )
}

export default App

