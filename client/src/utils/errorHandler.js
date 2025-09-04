import toast from 'react-hot-toast'

export const handleApiError = (error) => {
  const message = error?.response?.data?.message || error.message || 'An error occurred'

  if (message.includes('401')) {
    // Unauthorized - redirect to login
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    window.location.href = '/login'
  } else if (message.includes('403')) {
    // Forbidden - show access denied
    toast.error('Access denied')
  } else {
    // General error
    toast.error(message)
  }
}
