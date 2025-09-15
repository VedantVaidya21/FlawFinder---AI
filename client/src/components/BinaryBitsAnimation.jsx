import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

const BinaryBitsAnimation = ({ className = "", density = 'medium' }) => {
  const [binaryBits, setBinaryBits] = useState([])

  // Density configurations
  const densityConfig = {
    light: { count: 40, fontSize: '12px', opacity: 0.1 },
    medium: { count: 60, fontSize: '14px', opacity: 0.15 },
    heavy: { count: 80, fontSize: '16px', opacity: 0.2 }
  }

  const config = densityConfig[density] || densityConfig.medium

  useEffect(() => {
    const generateBinaryBits = () => {
      const bits = []
      for (let i = 0; i < config.count; i++) {
        bits.push({
          id: i,
          value: Math.random() > 0.5 ? '1' : '0',
          x: Math.random() * 100,
          y: Math.random() * 100,
          animationDelay: Math.random() * 5,
          animationDuration: 3 + Math.random() * 4,
          moveDirection: Math.random() > 0.5 ? 1 : -1,
          opacity: 0.3 + Math.random() * 0.4
        })
      }
      setBinaryBits(bits)
    }

    generateBinaryBits()

    // Regenerate bits periodically for dynamic effect
    const interval = setInterval(() => {
      setBinaryBits(prev => prev.map(bit => ({
        ...bit,
        value: Math.random() > 0.7 ? (bit.value === '1' ? '0' : '1') : bit.value
      })))
    }, 2000)

    return () => clearInterval(interval)
  }, [config.count])

  return (
    <div className={`absolute inset-0 overflow-hidden pointer-events-none ${className}`}>
      {binaryBits.map((bit) => (
        <motion.div
          key={bit.id}
          initial={{ 
            x: `${bit.x}%`, 
            y: `${bit.y}%`,
            opacity: 0
          }}
          animate={{
            x: `${bit.x + (bit.moveDirection * 10)}%`,
            y: `${bit.y - 20}%`,
            opacity: [0, bit.opacity, 0]
          }}
          transition={{
            duration: bit.animationDuration,
            repeat: Infinity,
            delay: bit.animationDelay,
            ease: "linear"
          }}
          className="absolute text-blue-400/30 font-mono select-none"
          style={{
            fontSize: config.fontSize,
            filter: 'blur(0.5px)'
          }}
        >
          {bit.value}
        </motion.div>
      ))}
      
      {/* Additional floating code symbols */}
      {[...Array(12)].map((_, i) => (
        <motion.div
          key={`symbol-${i}`}
          initial={{ 
            x: `${Math.random() * 100}%`,
            y: `${Math.random() * 100}%`,
            opacity: 0
          }}
          animate={{
            x: `${Math.random() * 100}%`,
            y: `${Math.random() * 100}%`,
            opacity: [0, 0.1, 0],
            rotate: [0, 360]
          }}
          transition={{
            duration: 8 + Math.random() * 4,
            repeat: Infinity,
            delay: Math.random() * 3,
            ease: "easeInOut"
          }}
          className="absolute text-purple-400/20 font-mono text-lg select-none"
        >
          {['<', '>', '/', '{', '}', '(', ')', '[', ']', '=', '+', '-'][Math.floor(Math.random() * 12)]}
        </motion.div>
      ))}
    </div>
  )
}

export default BinaryBitsAnimation
