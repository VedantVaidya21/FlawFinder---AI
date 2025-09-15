# FlawFinder AI - Frontend Integration Notes

This document provides essential information for integrating the FlawFinder AI frontend with the new backend.

## 🔗 API Base URL

Set the following environment variable in your frontend:

```javascript
// .env or environment configuration
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🔐 Authentication Integration

### 1. Update Login Flow

Replace the mock authentication in `Login.jsx` with real API calls:

```javascript
// In Login.jsx
const handleSubmit = async (e) => {
  e.preventDefault()
  
  if (!validateForm()) return
  
  setIsLoading(true)
  setErrors({})

  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    })

    const data = await response.json()

    if (response.ok) {
      // Store tokens
      localStorage.setItem('accessToken', data.access_token)
      localStorage.setItem('refreshToken', data.refresh_token)
      setIsAuthenticated(true)
      toast.success('Welcome to FlawFinder AI!')
      navigate('/dashboard')
    } else {
      toast.error(data.error?.message || 'Login failed')
      setErrors({ submit: data.error?.message || 'Login failed' })
    }
  } catch (error) {
    toast.error('Network error')
    setErrors({ submit: 'Network error' })
  } finally {
    setIsLoading(false)
  }
}
```

### 2. Create API Service

Create a new file `src/services/api.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const token = localStorage.getItem('accessToken')
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, config)
      
      if (response.status === 401) {
        // Token expired, try to refresh
        const refreshed = await this.refreshToken()
        if (refreshed) {
          // Retry the original request
          return this.request(endpoint, options)
        } else {
          // Redirect to login
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          window.location.href = '/login'
          return
        }
      }

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.error?.message || 'API request failed')
      }

      return data
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  async refreshToken() {
    const refreshToken = localStorage.getItem('refreshToken')
    if (!refreshToken) return false

    try {
      const response = await fetch(`${this.baseURL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken })
      })

      if (response.ok) {
        const data = await response.json()
        localStorage.setItem('accessToken', data.access_token)
        localStorage.setItem('refreshToken', data.refresh_token)
        return true
      }
    } catch (error) {
      console.error('Token refresh failed:', error)
    }

    return false
  }

  // Authentication methods
  async login(credentials) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    })
  }

  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  }

  async getCurrentUser() {
    return this.request('/auth/me')
  }

  // Process flows methods
  async createFlow(flowData) {
    return this.request('/flows', {
      method: 'POST',
      body: JSON.stringify(flowData)
    })
  }

  async getFlows() {
    return this.request('/flows')
  }

  async getFlow(id) {
    return this.request(`/flows/${id}`)
  }

  async parseFlow(id) {
    return this.request(`/flows/${id}/parse`, {
      method: 'POST'
    })
  }

  async getBrutalityScore(id) {
    return this.request(`/flows/${id}/score`)
  }

  async getRoleBasedFixes(id, role) {
    return this.request(`/flows/${id}/fixes?role=${role}`)
  }

  // Reports methods
  async generateCEOReport(reportData) {
    return this.request('/reports/ceo', {
      method: 'POST',
      body: JSON.stringify(reportData)
    })
  }

  async getReports() {
    return this.request('/reports')
  }

  async getReport(id) {
    return this.request(`/reports/${id}`)
  }

  // AgentOps methods
  async createPipeline(pipelineData) {
    return this.request('/agentops/pipelines', {
      method: 'POST',
      body: JSON.stringify(pipelineData)
    })
  }

  async getPipelines() {
    return this.request('/agentops/pipelines')
  }

  async getPipelineStatus(id) {
    return this.request(`/agentops/pipelines/${id}/status`)
  }
}

export const apiService = new ApiService()
```

## 📤 File Upload Integration

Update the Upload component to use the real API:

```javascript
// In Upload.jsx
const handleUpload = async () => {
  setIsUploading(true)
  setProgress(0)

  try {
    for (const file of files) {
      // Create FormData for file upload
      const formData = new FormData()
      formData.append('file', file)
      formData.append('name', file.name)
      formData.append('description', 'Uploaded workflow document')

      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/flows`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        },
        body: formData
      })

      if (response.ok) {
        const data = await response.json()
        toast.success(`File ${file.name} uploaded successfully`)
        // Navigate to flow details or dashboard
        navigate(`/flows/${data.id}`)
      } else {
        const error = await response.json()
        toast.error(`Upload failed: ${error.error?.message}`)
      }
    }
  } catch (error) {
    toast.error('Upload failed')
  } finally {
    setIsUploading(false)
  }
}
```

## 📊 Dashboard Integration

Update the Dashboard to fetch real data:

```javascript
// In Dashboard.jsx
const [flows, setFlows] = useState([])
const [brutalityScore, setBrutalityScore] = useState(0)

useEffect(() => {
  const fetchDashboardData = async () => {
    try {
      // Fetch user's flows
      const flowsData = await apiService.getFlows()
      setFlows(flowsData)

      // Calculate overall brutality score
      if (flowsData.length > 0) {
        const scores = await Promise.all(
          flowsData.map(flow => apiService.getBrutalityScore(flow.id))
        )
        const avgScore = scores.reduce((sum, score) => sum + score.score, 0) / scores.length
        setBrutalityScore(Math.round(avgScore))
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    }
  }

  fetchDashboardData()
}, [])
```

## 🔧 Fix Plan Integration

Update the FixPlan component:

```javascript
// In FixPlan.jsx
const [fixPlans, setFixPlans] = useState([])

useEffect(() => {
  const fetchFixPlans = async () => {
    try {
      const flows = await apiService.getFlows()
      const plans = await Promise.all(
        flows.map(async (flow) => {
          const fixes = await apiService.getRoleBasedFixes(flow.id, 'engineer')
          return {
            ...flow,
            fixes: fixes
          }
        })
      )
      setFixPlans(plans)
    } catch (error) {
      console.error('Failed to fetch fix plans:', error)
    }
  }

  fetchFixPlans()
}, [])
```

## 📈 CEO Report Integration

Update the CEOReport component:

```javascript
// In CEOReport.jsx
const handleGenerateReport = async () => {
  try {
    const report = await apiService.generateCEOReport({
      flow_id: selectedFlowId,
      include_departments: true,
      format: 'pdf'
    })
    
    toast.success('CEO report generated successfully')
    // Handle report display or download
  } catch (error) {
    toast.error('Failed to generate report')
  }
}
```

## 🚨 Error Handling

Implement consistent error handling:

```javascript
// Global error handler
const handleApiError = (error) => {
  if (error.message.includes('401')) {
    // Unauthorized - redirect to login
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    window.location.href = '/login'
  } else if (error.message.includes('403')) {
    // Forbidden - show access denied message
    toast.error('Access denied')
  } else {
    // General error
    toast.error(error.message || 'An error occurred')
  }
}
```

## 🔄 State Management

Consider using React Context for global state management:

```javascript
// src/contexts/AuthContext.jsx
import { createContext, useContext, useState, useEffect } from 'react'
import { apiService } from '../services/api'

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
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = async (credentials) => {
    const data = await apiService.login(credentials)
    localStorage.setItem('accessToken', data.access_token)
    localStorage.setItem('refreshToken', data.refresh_token)
    setUser(data.user)
    setIsAuthenticated(true)
    return data
  }

  const logout = () => {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    setUser(null)
    setIsAuthenticated(false)
  }

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated,
      loading,
      login,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
```

## 📝 Environment Variables

Create `.env` file in your frontend project:

```bash
# Frontend environment variables
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=FlawFinder AI
```

## 🔍 Testing the Integration

1. **Start the backend**:
   ```bash
   cd backend
   docker-compose up -d
   ```

2. **Start the frontend**:
   ```bash
   cd frontend-repo/client
   npm run dev
   ```

3. **Test the integration**:
   - Login with demo credentials: `admin@flawfinder.ai` / `password123`
   - Upload a workflow document
   - Generate a CEO report
   - Check the brutality score calculation

## 🐛 Common Issues

1. **CORS errors**: Ensure the backend CORS configuration includes your frontend URL
2. **Authentication errors**: Check that JWT tokens are being sent correctly
3. **File upload issues**: Verify the file size and format restrictions
4. **Network errors**: Ensure the backend is running and accessible

## 📞 Support

For integration issues:
1. Check the browser console for error messages
2. Verify the API endpoints are responding correctly
3. Check the backend logs for server-side errors
4. Review the OpenAPI documentation at `http://localhost:8000/docs` 