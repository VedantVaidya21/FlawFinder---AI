import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useAuth } from './contexts/AuthContext'
import { Toaster } from 'react-hot-toast'
import { motion } from 'framer-motion'
import { ThemeProvider } from './contexts/ThemeContext'
import { AuthProvider } from './contexts/AuthContext'
import Landing from './pages/Landing'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import FixPlan from './pages/FixPlan'
import CEOReport from './pages/CEOReport'
import Navigation from './components/Navigation'

function App() {
  const { isAuthenticated } = useAuth()

  return (
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
            element={<Landing />} 
          />
          <Route path="/login" element={<Login />} />

          <Route 
            path="/signup" 
            element={<Signup />} 
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
  )
}

const AppWrapper = () => (
  <AuthProvider>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </AuthProvider>
)

export default AppWrapper
