import { useEffect, useRef, useState } from 'react'
import { motion, useScroll, useTransform, useInView, useAnimation } from 'framer-motion'
import { useSpring, animated, useSpringValue } from '@react-spring/web'
import { ArrowRight, Play, CheckCircle, Users, TrendingUp, Shield, Zap, Globe, ArrowDown, Binary, Code, Cpu } from 'lucide-react'
import { Link } from 'react-router-dom'

// Binary Bits Animation Component
const BinaryBitsAnimation = ({ opacity = 0.05 }) => {
  const [bits, setBits] = useState([])
  
  useEffect(() => {
    const generateBits = () => {
      const newBits = []
      for (let i = 0; i < 50; i++) {
        newBits.push({
          id: i,
          x: Math.random() * 100,
          y: Math.random() * 100,
          value: Math.random() > 0.5 ? '1' : '0',
          size: Math.random() * 0.5 + 0.3,
          speed: Math.random() * 0.02 + 0.01
        })
      }
      setBits(newBits)
    }
    
    generateBits()
    const interval = setInterval(() => {
      setBits(prev => prev.map(bit => ({
        ...bit,
        y: (bit.y + bit.speed) % 100,
        value: Math.random() > 0.98 ? (Math.random() > 0.5 ? '1' : '0') : bit.value
      })))
    }, 50)
    
    return () => clearInterval(interval)
  }, [])
  
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      {bits.map(bit => (
        <div
          key={bit.id}
          className="absolute text-blue-400 font-mono transition-all duration-100"
          style={{
            left: `${bit.x}%`,
            top: `${bit.y}%`,
            fontSize: `${bit.size}rem`,
            opacity: opacity
          }}
        >
          {bit.value}
        </div>
      ))}
    </div>
  )
}

const Landing = () => {
  const [isVideoPlaying, setIsVideoPlaying] = useState(false)
  const videoRef = useRef(null)
  const { scrollYProgress } = useScroll()
  const heroRef = useRef(null)
  const featuresRef = useRef(null)
  const statsRef = useRef(null)
  
  const heroInView = useInView(heroRef, { once: true })
  const featuresInView = useInView(featuresRef, { once: true })
  const statsInView = useInView(statsRef, { once: true })

  // Advanced Apple-inspired parallax transforms
  const heroY = useTransform(scrollYProgress, [0, 0.5], [0, -200])
  const videoY = useTransform(scrollYProgress, [0, 0.5], [0, 150])
  const textY = useTransform(scrollYProgress, [0, 0.5], [0, -150])
  const opacityFade = useTransform(scrollYProgress, [0, 0.3], [1, 0])
  const scale = useTransform(scrollYProgress, [0, 0.3], [1, 0.8])
  
  // React Spring parallax for smooth performance
  const [{ scrollY }, set] = useSpring(() => ({ scrollY: 0 }))
  
  useEffect(() => {
    const handleScroll = () => {
      set({ scrollY: window.scrollY })
    }
    
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleVideoPlay = () => {
    if (videoRef.current) {
      if (isVideoPlaying) {
        videoRef.current.pause()
      } else {
        videoRef.current.play()
      }
      setIsVideoPlaying(!isVideoPlaying)
    }
  }

  const stats = [
    { number: '10,000+', label: 'Companies Trust Us', icon: Users },
    { number: '99.9%', label: 'Uptime Guarantee', icon: Shield },
    { number: '50+', label: 'Countries Served', icon: Globe },
    { number: '24/7', label: 'Expert Support', icon: Zap }
  ]

  const features = [
    {
      title: 'AI-Powered Analysis',
      description: 'Advanced machine learning algorithms analyze your business workflows to identify inefficiencies and bottlenecks.',
      icon: TrendingUp,
      color: 'from-blue-500 to-blue-600'
    },
    {
      title: 'Real-Time Monitoring',
      description: 'Continuous monitoring of your operations with instant alerts when issues are detected.',
      icon: Zap,
      color: 'from-purple-500 to-purple-600'
    },
    {
      title: 'Enterprise Security',
      description: 'Bank-level encryption and compliance with industry standards to protect your sensitive data.',
      icon: Shield,
      color: 'from-green-500 to-green-600'
    },
    {
      title: 'Global Scale',
      description: 'Built to handle enterprise-level workloads with 99.9% uptime and global infrastructure.',
      icon: Globe,
      color: 'from-orange-500 to-orange-600'
    }
  ]

  return (
    <div className="bg-white text-gray-900 overflow-hidden">
      {/* Hero Section */}
      <motion.section 
        ref={heroRef}
        style={{ y: heroY }}
        className="relative min-h-screen flex items-center justify-center"
      >
        {/* Video Background */}
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            style={{ y: videoY }}
            className="absolute inset-0 w-full h-full"
          >
            <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-black/20 to-black/60 z-10" />
            <video
              ref={videoRef}
              className="w-full h-full object-cover"
              loop
              muted
              playsInline
              poster="https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1920&auto=format&fit=crop"
            >
              <source src="https://player.vimeo.com/external/371433846.sd.mp4?s=236da2f3c0fd273d2c6d9a064f3ae35579b2bbdf&profile_id=165&oauth2_token_id=57447761" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </motion.div>
        </div>

        {/* Binary Bits Background */}
        <BinaryBitsAnimation opacity={0.03} />
        
        {/* Hero Content */}
        <div className="relative z-20 text-center text-white px-4 max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={heroInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
            style={{ y: textY, opacity: opacityFade, scale }}
          >
            <h1 className="text-5xl md:text-7xl font-light mb-6 leading-tight">
              The Future of
              <span className="block font-semibold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Business Intelligence
              </span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-gray-200 max-w-3xl mx-auto font-light">
              FlawFinder AI revolutionizes how enterprises identify and resolve operational inefficiencies with cutting-edge artificial intelligence.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link to="/signup">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="bg-white text-gray-900 px-8 py-4 rounded-full font-semibold text-lg hover:bg-gray-100 transition-colors flex items-center gap-2"
                >
                  Get Started
                  <ArrowRight className="w-5 h-5" />
                </motion.button>
              </Link>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleVideoPlay}
                className="border-2 border-white text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-white hover:text-gray-900 transition-colors flex items-center gap-2"
              >
                <Play className="w-5 h-5" />
                Watch Demo
              </motion.button>
            </div>
          </motion.div>
        </div>

        {/* Scroll Indicator */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.5, duration: 0.5 }}
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2 text-white z-20"
        >
          <motion.div
            animate={{ y: [0, 10, 0] }}
            transition={{ repeat: Infinity, duration: 1.5 }}
            className="flex flex-col items-center"
          >
            <span className="text-sm mb-2">Scroll to explore</span>
            <ArrowDown className="w-6 h-6" />
          </motion.div>
        </motion.div>
      </motion.section>

      {/* Stats Section */}
      <motion.section 
        ref={statsRef}
        className="py-20 bg-gray-50"
      >
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => {
              const Icon = stat.icon
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 40 }}
                  animate={statsInView ? { opacity: 1, y: 0 } : {}}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="text-center"
                >
                  <div className="mb-4 flex justify-center">
                    <Icon className="w-8 h-8 text-blue-600" />
                  </div>
                  <div className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                    {stat.number}
                  </div>
                  <div className="text-gray-600">
                    {stat.label}
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>
      </motion.section>

      {/* Features Section */}
      <motion.section 
        ref={featuresRef}
        className="py-20 bg-white"
      >
        <div className="max-w-7xl mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={featuresInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-light mb-6 text-gray-900">
              Built for the Modern Enterprise
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Discover how FlawFinder AI transforms your business operations with intelligent automation and insights.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 40 }}
                  animate={featuresInView ? { opacity: 1, y: 0 } : {}}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  whileHover={{ y: -5 }}
                  className="p-6 rounded-2xl bg-gray-50 hover:bg-gray-100 transition-all duration-300"
                >
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3 text-gray-900">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </p>
                </motion.div>
              )
            })}
          </div>
        </div>
      </motion.section>

      {/* CTA Section */}
      <motion.section className="py-20 bg-gradient-to-br from-blue-600 to-purple-700 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-light mb-6">
              Ready to Transform Your Business?
            </h2>
            <p className="text-xl mb-8 text-blue-100">
              Join thousands of companies already using FlawFinder AI to optimize their operations.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/signup">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="bg-white text-blue-600 px-8 py-4 rounded-full font-semibold text-lg hover:bg-gray-100 transition-colors"
                >
                  Start Free Trial
                </motion.button>
              </Link>
              <Link to="/login">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="border-2 border-white text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-white hover:text-blue-600 transition-colors"
                >
                  Sign In
                </motion.button>
              </Link>
            </div>
          </motion.div>
        </div>
      </motion.section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                  <Zap className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold">FlawFinder AI</span>
              </div>
              <p className="text-gray-400">
                Revolutionizing business operations with artificial intelligence.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 FlawFinder AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Landing
