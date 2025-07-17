import { motion } from 'framer-motion'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useTheme } from '../contexts/ThemeContext'
import { 
  Home, 
  Upload, 
  FileText, 
  BarChart3, 
  Settings, 
  Moon, 
  Sun,
  LogOut,
  Zap
} from 'lucide-react'
import toast from 'react-hot-toast'
import { useState } from 'react'

const Navigation = ({ isDark, toggleTheme, location, navigate, showLogoutModal, setShowLogoutModal, handleLogout }) => {
  const navItems = [
    { path: '/dashboard', icon: Home, label: 'Dashboard' },
    { path: '/upload', icon: Upload, label: 'Upload' },
    { path: '/fix-plan', icon: FileText, label: 'Fix Plan' },
    { path: '/ceo-report', icon: BarChart3, label: 'CEO Report' },
  ]

  return (
    <motion.nav
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="glass-dark border-b border-zinc-700/30 backdrop-blur-xl sticky top-0 z-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center space-x-3"
          >
            <div className="relative">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                className="w-10 h-10 bg-gradient-to-r from-purple-500 to-primary-500 rounded-lg flex items-center justify-center shadow-glow"
              >
                <Zap className="w-6 h-6 text-white" />
              </motion.div>
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                className="absolute inset-0 bg-gradient-to-r from-purple-500 to-primary-500 rounded-lg opacity-30 blur-sm"
              />
            </div>
            <div>
              <h1 className="text-xl font-bold glow-text">FlawFinder</h1>
              <p className="text-xs text-zinc-1000 -mt-1">AI-Powered</p>
            </div>
          </motion.div>

          {/* Navigation Items */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              
              return (
                <motion.div
                  key={item.path}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Link
                    to={item.path}
                    className={`relative flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-300 ${
                      isActive
                        ? 'bg-gradient-to-r from-purple-600 to-primary-600 text-white shadow-glow'
                        : 'text-zinc-1000 hover:text-zinc-100 hover:bg-zinc-700/30'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.label}</span>
                    {isActive && (
                      <motion.div
                        layoutId="activeTab"
                        className="absolute inset-0 bg-gradient-to-r from-purple-600 to-primary-600 rounded-lg -z-10"
                        transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                      />
                    )}
                  </Link>
                </motion.div>
              )
            })}
          </div>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-3">
            {/* Theme Toggle */}
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={toggleTheme}
              className="relative p-2 rounded-lg bg-zinc-700/30 hover:bg-zinc-700/50 transition-all duration-300 group"
            >
              <motion.div
                animate={{ rotate: isDark ? 0 : 180 }}
                transition={{ duration: 0.5, ease: "easeInOut" }}
              >
                {isDark ? (
                  <Sun className="w-5 h-5 text-yellow-400" />
                ) : (
                  <Moon className="w-5 h-5 text-purple-400" />
                )}
              </motion.div>
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500 to-primary-500 rounded-lg opacity-0 group-hover:opacity-20 transition-opacity duration-300" />
            </motion.button>

            {/* Settings */}
            <motion.button
              whileHover={{ scale: 1.1, rotate: 90 }}
              whileTap={{ scale: 0.9 }}
              className="p-2 rounded-lg bg-zinc-700/30 hover:bg-zinc-700/50 transition-all duration-300 text-zinc-1000 hover:text-zinc-100"
            >
              <Settings className="w-5 h-5" />
            </motion.button>

            {/* Logout */}
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => setShowLogoutModal(true)}
              className="p-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 transition-all duration-300 text-red-400 hover:text-red-300"
            >
              <LogOut className="w-5 h-5" />
            </motion.button>
          </div>
        </div>
      </div>
    </motion.nav>
  )
}

// Logout Confirmation Modal rendered outside the nav for proper centering
const LogoutModal = ({ show, onCancel, onConfirm, isDark }) => {
  if (!show) return null
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className={`rounded-xl p-6 shadow-lg w-80 ${isDark ? 'bg-zinc-900 text-white' : 'bg-white text-zinc-900'}`}>
        <h2 className="text-lg font-semibold mb-2">Confirm Logout</h2>
        <p className="mb-4">Are you sure you want to log out?</p>
        <div className="flex justify-end space-x-3">
          <button
            onClick={onCancel}
            className={`px-4 py-2 rounded-lg border ${isDark ? 'border-zinc-700 text-zinc-200 hover:bg-zinc-800' : 'border-zinc-300 text-zinc-800 hover:bg-zinc-100'} transition-all cursor-pointer`}
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className="px-4 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600 transition-all cursor-pointer"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  )
}

const NavigationWithModal = () => {
  const { isDark, toggleTheme } = useTheme()
  const location = useLocation()
  const navigate = useNavigate()
  const [showLogoutModal, setShowLogoutModal] = useState(false)

  const handleLogout = () => {
    localStorage.removeItem('authToken')
    toast.success('Logged out successfully')
    navigate('/')
    window.location.reload()
  }

  return (
    <>
      <Navigation
        isDark={isDark}
        toggleTheme={toggleTheme}
        location={location}
        navigate={navigate}
        showLogoutModal={showLogoutModal}
        setShowLogoutModal={setShowLogoutModal}
        handleLogout={handleLogout}
      />
      <LogoutModal
        show={showLogoutModal}
        onCancel={() => setShowLogoutModal(false)}
        onConfirm={() => { setShowLogoutModal(false); handleLogout(); }}
        isDark={isDark}
      />
    </>
  )
}

export default NavigationWithModal

