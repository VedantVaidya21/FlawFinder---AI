import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import toast from 'react-hot-toast'
import { motion } from 'framer-motion'
import { Lock, LogIn, Zap, Eye, EyeOff, Shield, Sparkles, ArrowRight, Mail, Github, Chrome } from 'lucide-react'

const Login = ({ setIsAuthenticated }) => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [errors, setErrors] = useState({})
  const navigate = useNavigate()

  const validateForm = () => {
    const newErrors = {}
    
    if (!email) {
      newErrors.email = 'Email is required'
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Please enter a valid email address'
    }
    
    if (!password) {
      newErrors.password = 'Password is required'
    } else if (password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return
    
    setIsLoading(true)
    setErrors({})

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Mock authentication process (replace with your own logic)
    if (email === 'admin@flawfinder.ai' && password === 'password123') {
      localStorage.setItem('authToken', '12345')
      setIsAuthenticated(true)
      toast.success('Welcome to FlawFinder AI!')
      navigate('/dashboard')
    } else {
      toast.error('Invalid email or password')
      setErrors({ submit: 'Invalid email or password. Please try again.' })
    }
    setIsLoading(false)
  }

  const handleGoogleLogin = async () => {
    setIsLoading(true)
    // Simulate Google OAuth process
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    localStorage.setItem('authToken', 'google12345')
    setIsAuthenticated(true)
    toast.success('Logged in with Google')
    navigate('/dashboard')
    setIsLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-950 relative overflow-hidden">
      {/* Enhanced Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Primary orbs */}
        <motion.div
          animate={{
            x: [0, 150, 0],
            y: [0, -75, 0],
            rotate: [0, 360]
          }}
          transition={{
            duration: 30,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute -top-48 -left-48 w-96 h-96 bg-gradient-to-r from-blue-500/30 to-purple-500/30 rounded-full blur-3xl"
        />
        <motion.div
          animate={{
            x: [0, -120, 0],
            y: [0, 120, 0],
            rotate: [360, 0]
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute -bottom-48 -right-48 w-96 h-96 bg-gradient-to-l from-purple-500/30 to-pink-500/30 rounded-full blur-3xl"
        />
        <motion.div
          animate={{
            x: [0, 80, 0],
            y: [0, -120, 0],
            scale: [1, 1.2, 1]
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[32rem] h-[32rem] bg-gradient-to-r from-indigo-500/15 to-purple-500/15 rounded-full blur-3xl"
        />
        
        {/* Secondary accent orbs */}
        <motion.div
          animate={{
            x: [0, -60, 0],
            y: [0, 60, 0],
            opacity: [0.3, 0.8, 0.3]
          }}
          transition={{
            duration: 18,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute top-1/4 right-1/4 w-64 h-64 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-full blur-2xl"
        />
        <motion.div
          animate={{
            x: [0, 40, 0],
            y: [0, -80, 0],
            opacity: [0.4, 0.7, 0.4]
          }}
          transition={{
            duration: 22,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute bottom-1/4 left-1/4 w-48 h-48 bg-gradient-to-l from-violet-500/25 to-purple-500/25 rounded-full blur-2xl"
        />
      </div>

      {/* Enhanced Grid Pattern */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2280%22%20height%3D%2280%22%20viewBox%3D%220%200%2080%2080%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%23ffffff%22%20fill-opacity%3D%220.03%22%3E%3Ccircle%20cx%3D%2240%22%20cy%3D%2240%22%20r%3D%221%22%3E%3C/circle%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-40"></div>
      
      {/* Subtle noise texture */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg%20viewBox%3D%220%200%20200%20200%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cfilter%20id%3D%22noiseFilter%22%3E%3CfeTurbulence%20type%3D%22fractalNoise%22%20baseFrequency%3D%220.85%22%20numOctaves%3D%224%22%20stitchTiles%3D%22stitch%22/%3E%3C/filter%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20filter%3D%22url(%23noiseFilter)%22%20opacity%3D%220.4%22/%3E%3C/svg%3E')] opacity-[0.015] mix-blend-overlay"></div>

      <div className="relative z-10 flex min-h-screen">
        {/* Left Side - Enhanced Hero Section */}
        <div className="hidden lg:flex lg:w-1/2 flex-col justify-center items-center p-12 text-center relative">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-lg z-10"
          >
            {/* Enhanced Logo */}
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="flex items-center justify-center mb-8"
            >
              <motion.div
                whileHover={{ scale: 1.05, rotate: 5 }}
                className="relative"
              >
                <div className="w-24 h-24 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-3xl flex items-center justify-center shadow-2xl shadow-purple-500/40">
                  <Zap className="w-12 h-12 text-white" />
                </div>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                  className="absolute -inset-2 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-3xl blur opacity-30"
                />
                <motion.div
                  animate={{ scale: [1, 1.1, 1] }}
                  transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                  className="absolute -inset-1 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 rounded-3xl blur-sm opacity-20"
                />
              </motion.div>
            </motion.div>

            {/* Enhanced Title */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="text-6xl font-bold bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent mb-4 tracking-tight"
            >
              FlawFinder AI
            </motion.h1>

            {/* Enhanced Subtitle */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6, duration: 0.6 }}
              className="text-xl text-gray-300 mb-10 font-light leading-relaxed"
            >
              Intelligent. Precise. Transformative.
              <br />
              <span className="text-lg text-blue-200 opacity-90">Revolutionizing code analysis with AI</span>
            </motion.p>

            {/* Enhanced Feature List */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8, duration: 0.6 }}
              className="space-y-5 text-left"
            >
              {[
                { icon: Shield, text: 'Advanced AI-powered vulnerability detection', color: 'from-emerald-400 to-cyan-400' },
                { icon: Sparkles, text: 'Real-time code analysis & optimization', color: 'from-purple-400 to-pink-400' },
                { icon: ArrowRight, text: 'Automated fix recommendations', color: 'from-blue-400 to-indigo-400' }
              ].map((item, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 1 + index * 0.2, duration: 0.5 }}
                  whileHover={{ x: 5 }}
                  className="flex items-center space-x-4 text-gray-200 group cursor-default"
                >
                  <div className={`w-10 h-10 bg-gradient-to-r ${item.color} rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg group-hover:shadow-xl transition-all duration-300`}>
                    <item.icon className="w-5 h-5 text-white" />
                  </div>
                  <span className="text-sm font-medium group-hover:text-white transition-colors duration-300">{item.text}</span>
                </motion.div>
              ))}
            </motion.div>

            {/* Trust indicators */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.6, duration: 0.6 }}
              className="mt-10 flex items-center justify-center space-x-6 text-gray-400"
            >
              <div className="text-center">
                <div className="text-lg font-semibold text-white">99.9%</div>
                <div className="text-xs">Uptime</div>
              </div>
              <div className="w-px h-8 bg-gray-600"></div>
              <div className="text-center">
                <div className="text-lg font-semibold text-white">10K+</div>
                <div className="text-xs">Companies</div>
              </div>
              <div className="w-px h-8 bg-gray-600"></div>
              <div className="text-center">
                <div className="text-lg font-semibold text-white">24/7</div>
                <div className="text-xs">Support</div>
              </div>
            </motion.div>
          </motion.div>
        </div>

        {/* Right Side - Enhanced Login Form */}
        <div className="w-full lg:w-1/2 flex items-center justify-center p-6 lg:p-12">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
            className="w-full max-w-md"
          >
            {/* Enhanced Main Login Card */}
            <div className="bg-white/[0.03] backdrop-blur-2xl border border-white/[0.08] rounded-3xl p-8 shadow-2xl relative overflow-hidden">
              {/* Card background glow */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/5 to-pink-500/5 rounded-3xl"></div>
              
              {/* Header */}
              <div className="text-center mb-8 relative z-10">
                <motion.div
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 0.2, duration: 0.5 }}
                  whileHover={{ scale: 1.05 }}
                  className="w-18 h-18 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-xl shadow-purple-500/30"
                >
                  <Lock className="w-8 h-8 text-white" />
                </motion.div>
                <h2 className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-2">Welcome Back</h2>
                <p className="text-gray-400 text-sm font-light">Sign in to continue to FlawFinder AI</p>
              </div>

              {/* Error Message */}
              {errors.submit && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-300 text-sm"
                >
                  {errors.submit}
                </motion.div>
              )}

              {/* Enhanced Form */}
              <form onSubmit={handleSubmit} className="space-y-6 relative z-10">
                {/* Email Field */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-3">Email Address</label>
                  <div className="relative group">
                    <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5 transition-colors group-focus-within:text-purple-400" />
                    <input
                      type="email"
                      placeholder="Enter your email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className={`w-full px-4 py-4 pl-12 bg-white/[0.03] border rounded-2xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all duration-300 font-medium ${
                        errors.email ? 'border-red-500/50 focus:ring-red-500/50' : 'border-white/10 hover:border-white/20'
                      }`}
                    />
                    {errors.email && (
                      <motion.p
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-2 text-sm text-red-400 font-medium"
                      >
                        {errors.email}
                      </motion.p>
                    )}
                  </div>
                </div>

                {/* Password Field */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-3">Password</label>
                  <div className="relative group">
                    <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5 transition-colors group-focus-within:text-purple-400" />
                    <input
                      type={showPassword ? "text" : "password"}
                      placeholder="Enter your password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className={`w-full px-4 py-4 pl-12 pr-12 bg-white/[0.03] border rounded-2xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all duration-300 font-medium ${
                        errors.password ? 'border-red-500/50 focus:ring-red-500/50' : 'border-white/10 hover:border-white/20'
                      }`}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors p-1 rounded-lg hover:bg-white/5"
                    >
                      {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                    {errors.password && (
                      <motion.p
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-2 text-sm text-red-400 font-medium"
                      >
                        {errors.password}
                      </motion.p>
                    )}
                  </div>
                </div>

                {/* Remember Me & Forgot Password */}
                <div className="flex items-center justify-between">
                  <label className="flex items-center space-x-2 cursor-pointer group">
                    <input type="checkbox" className="w-4 h-4 text-purple-500 bg-white/5 border-white/10 rounded focus:ring-purple-500 focus:ring-2" />
                    <span className="text-sm text-gray-400 group-hover:text-gray-300 transition-colors">Remember me</span>
                  </label>
                  <Link to="#" className="text-sm text-purple-400 hover:text-purple-300 transition-colors font-medium">
                    Forgot password?
                  </Link>
                </div>

                {/* Enhanced Login Button */}
                <motion.button
                  whileHover={{ scale: 1.02, y: -2 }}
                  whileTap={{ scale: 0.98 }}
                  type="submit"
                  disabled={isLoading}
                  className="w-full py-4 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 text-white font-semibold rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden group"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  <div className="relative z-10 flex items-center">
                    {isLoading ? (
                      <>
                        <motion.div
                          animate={{ rotate: 360 }}
                          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                          className="w-5 h-5 border-2 border-white border-t-transparent rounded-full mr-2"
                        />
                        Signing in...
                      </>
                    ) : (
                      <>
                        <LogIn className="w-5 h-5 mr-2" />
                        Sign In
                      </>
                    )}
                  </div>
                </motion.button>
              </form>

              {/* Enhanced Divider */}
              <div className="relative my-8">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-white/10"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-6 bg-white/[0.02] text-gray-400 font-medium">Or continue with</span>
                </div>
              </div>

              {/* Social Login Buttons */}
              <div className="space-y-3">
                <motion.button
                  whileHover={{ scale: 1.02, y: -1 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleGoogleLogin}
                  disabled={isLoading}
                  className="w-full py-3 bg-white/[0.03] border border-white/10 text-white font-medium rounded-2xl hover:bg-white/[0.06] hover:border-white/20 transition-all duration-300 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed group"
                >
                  <svg className="w-5 h-5 mr-3 group-hover:scale-110 transition-transform duration-300" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                  </svg>
                  Continue with Google
                </motion.button>
                
                <motion.button
                  whileHover={{ scale: 1.02, y: -1 }}
                  whileTap={{ scale: 0.98 }}
                  disabled={isLoading}
                  className="w-full py-3 bg-white/[0.03] border border-white/10 text-white font-medium rounded-2xl hover:bg-white/[0.06] hover:border-white/20 transition-all duration-300 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed group"
                >
                  <Github className="w-5 h-5 mr-3 group-hover:scale-110 transition-transform duration-300" />
                  Continue with GitHub
                </motion.button>
              </div>

              {/* Sign Up Link */}
              <div className="mt-8 text-center">
                <p className="text-gray-400 text-sm">
                  Don't have an account?{' '}
                  <Link to="/signup" className="text-purple-400 hover:text-purple-300 transition-colors font-medium">
                    Create one here
                  </Link>
                </p>
              </div>
            </div>

            {/* Enhanced Demo Credentials */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8, duration: 0.6 }}
              className="mt-6 p-5 bg-white/[0.02] backdrop-blur-sm border border-white/10 rounded-3xl relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/5 via-blue-500/5 to-purple-500/5"></div>
              <div className="relative z-10">
                <h3 className="text-sm font-semibold text-white mb-3 flex items-center">
                  <Lock className="w-4 h-4 mr-2 text-emerald-400" />
                  Demo Credentials
                </h3>
                <div className="text-sm text-gray-300 space-y-2">
                  <div className="flex items-center justify-between p-2 bg-white/5 rounded-lg">
                    <span className="text-gray-400">Email:</span>
                    <span className="font-mono text-blue-300">admin@flawfinder.ai</span>
                  </div>
                  <div className="flex items-center justify-between p-2 bg-white/5 rounded-lg">
                    <span className="text-gray-400">Password:</span>
                    <span className="font-mono text-blue-300">password123</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default Login


