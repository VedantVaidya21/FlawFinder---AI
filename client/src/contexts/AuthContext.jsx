import { createContext, useContext, useState, useEffect } from 'react'
import { apiService } from '../services/api'
import { toast } from 'react-hot-toast'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      apiService.getCurrentUser()
        .then(userData => {
          setUser(userData)
          setIsAuthenticated(true)
        })
        .catch(() => {
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          toast.error('Session expired, please login again')
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  // Normal login via API
  const login = async (credentials) => {
    const tokenData = await apiService.login(credentials);
    localStorage.setItem('accessToken', tokenData.access_token);
    localStorage.setItem('refreshToken', tokenData.refresh_token);
    
    // After setting the token, get user data
    const userData = await apiService.getCurrentUser();
    setUser(userData);
    setIsAuthenticated(true);
    
    return userData;
  }

  // Logout function
  const logout = () => {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    setUser(null)
    setIsAuthenticated(false)
  }

  // Demo login for local testing
  const demoLogin = () => {
    const demoUser = {
      name: 'Vedant Vaidyar',
      email: 'admin@flawfinder.ai',
      role: 'admin'
    }

    // Save fake tokens so session persists
    localStorage.setItem('accessToken', 'demo-access-token')
    localStorage.setItem('refreshToken', 'demo-refresh-token')

    setUser(demoUser)
    setIsAuthenticated(true)
    toast.success('Logged in as Demo User')
  }

  return (
    <AuthContext.Provider value={{ 
      user, 
      isAuthenticated, 
      loading, 
      login, 
      logout, 
      demoLogin // added demo login
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
