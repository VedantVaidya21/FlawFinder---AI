import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, ChevronUp, Copy, CheckCircle, AlertTriangle, Zap, Users, Clock, DollarSign } from 'lucide-react'
import toast from 'react-hot-toast'

const mockFixPlans = [
  {
    id: 1,
    flaw: 'Inefficient approval process',
    severity: 'High',
    department: 'HR',
    impact: 85,
    estimatedCost: '$2,500',
    timeline: '2 weeks',
    fixes: [
      {
        title: 'Implement automated workflow approval system',
        description: 'Deploy a digital approval system that routes requests automatically based on predefined rules.',
        tools: ['Zapier', 'Microsoft Power Automate', 'Workflow automation software'],
        steps: [
          'Map current approval workflow',
          'Define approval rules and criteria',
          'Set up automated routing system',
          'Test with pilot group',
          'Full rollout and training'
        ]
      },
      {
        title: 'Reduce approval levels',
        description: 'Streamline the approval process by reducing unnecessary approval steps.',
        tools: ['Process mapping software', 'Organizational chart tools'],
        steps: [
          'Analyze current approval hierarchy',
          'Identify redundant approval levels',
          'Design new streamlined process',
          'Get stakeholder buy-in',
          'Implement new process'
        ]
      }
    ]
  },
  {
    id: 2,
    flaw: 'Manual inventory tracking',
    severity: 'High',
    department: 'Operations',
    impact: 90,
    estimatedCost: '$5,000',
    timeline: '3 weeks',
    fixes: [
      {
        title: 'Implement barcode scanning system',
        description: 'Deploy barcode scanners and inventory management software for real-time tracking.',
        tools: ['Barcode scanners', 'Inventory management software', 'Mobile devices'],
        steps: [
          'Choose inventory management software',
          'Purchase barcode scanners',
          'Create barcode labels for all items',
          'Train staff on new system',
          'Migrate existing data'
        ]
      }
    ]
  },
  {
    id: 3,
    flaw: 'Duplicate data entry',
    severity: 'Medium',
    department: 'Finance',
    impact: 65,
    estimatedCost: '$1,200',
    timeline: '1 week',
    fixes: [
      {
        title: 'Integrate systems to eliminate duplicate entry',
        description: 'Connect existing systems to automatically sync data and eliminate manual duplication.',
        tools: ['API integration tools', 'Data synchronization software'],
        steps: [
          'Map data flow between systems',
          'Set up API connections',
          'Configure automatic sync rules',
          'Test data integrity',
          'Monitor and optimize'
        ]
      }
    ]
  }
]

const FixPlan = () => {
  const [expandedItems, setExpandedItems] = useState({})

  const toggleExpanded = (id) => {
    setExpandedItems(prev => ({
      ...prev,
      [id]: !prev[id]
    }))
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    toast.success('Copied to clipboard!')
  }

  return (
    <div className="min-h-screen bg-zinc-900 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold glow-text mb-2">Fix Plan</h1>
          <p className="text-zinc-1000">Detailed solutions and recommendations for detected flaws</p>
        </motion.div>

        {/* Fix Plans */}
        <div className="space-y-6">
          {mockFixPlans.map((plan, index) => (
            <motion.div
              key={plan.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="glass-dark rounded-2xl border border-zinc-700/30 overflow-hidden"
            >
              {/* Header */}
              <div
                className="p-6 cursor-pointer hover:bg-zinc-700/20 transition-colors"
                onClick={() => toggleExpanded(plan.id)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <div className={`w-3 h-3 rounded-full ${
                        plan.severity === 'High' ? 'bg-red-500' :
                        plan.severity === 'Medium' ? 'bg-yellow-500' : 'bg-green-500'
                      }`} />
                      <h3 className="text-lg font-semibold text-zinc-100">{plan.flaw}</h3>
                      <span className="text-xs text-zinc-1000 bg-zinc-700/50 px-2 py-1 rounded-full">
                        {plan.department}
                      </span>
                    </div>
                    
                    {/* Quick stats */}
                    <div className="flex items-center space-x-6 text-sm text-zinc-1000">
                      <div className="flex items-center space-x-1">
                        <AlertTriangle className="w-4 h-4" />
                        <span>{plan.impact}% impact</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <DollarSign className="w-4 h-4" />
                        <span>{plan.estimatedCost}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Clock className="w-4 h-4" />
                        <span>{plan.timeline}</span>
                      </div>
                    </div>
                  </div>
                  
                  <motion.div
                    animate={{ rotate: expandedItems[plan.id] ? 180 : 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <ChevronDown className="w-5 h-5 text-zinc-1000" />
                  </motion.div>
                </div>
              </div>

              {/* Expanded Content */}
              <AnimatePresence>
                {expandedItems[plan.id] && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="border-t border-zinc-700/30"
                  >
                    <div className="p-6 space-y-6">
                      {plan.fixes.map((fix, fixIndex) => (
                        <motion.div
                          key={fixIndex}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: fixIndex * 0.1 }}
                          className="bg-zinc-800/30 rounded-xl p-5 border border-zinc-700/20"
                        >
                          <div className="flex items-start justify-between mb-4">
                            <div className="flex items-center space-x-2">
                              <Zap className="w-5 h-5 text-purple-400 flex-shrink-0" />
                              <h4 className="text-lg font-semibold text-zinc-100">{fix.title}</h4>
                            </div>
                            <motion.button
                              whileHover={{ scale: 1.05 }}
                              whileTap={{ scale: 0.95 }}
                              onClick={() => copyToClipboard(fix.title)}
                              className="p-2 rounded-lg bg-zinc-700/50 hover:bg-zinc-700/70 transition-colors"
                            >
                              <Copy className="w-4 h-4 text-zinc-1000" />
                            </motion.button>
                          </div>
                          
                          <p className="text-zinc-600 mb-4">{fix.description}</p>
                          
                          {/* Tools */}
                          <div className="mb-4">
                            <h5 className="text-sm font-medium text-zinc-600 mb-2 flex items-center">
                              <Users className="w-4 h-4 mr-1" />
                              Recommended Tools
                            </h5>
                            <div className="flex flex-wrap gap-2">
                              {fix.tools.map((tool, toolIndex) => (
                                <motion.span
                                  key={toolIndex}
                                  initial={{ opacity: 0, scale: 0.8 }}
                                  animate={{ opacity: 1, scale: 1 }}
                                  transition={{ delay: toolIndex * 0.05 }}
                                  className="inline-flex items-center px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-sm cursor-pointer hover:bg-purple-500/30 transition-colors"
                                  onClick={() => copyToClipboard(tool)}
                                >
                                  {tool}
                                </motion.span>
                              ))}
                            </div>
                          </div>
                          
                          {/* Steps */}
                          <div>
                            <h5 className="text-sm font-medium text-zinc-600 mb-3 flex items-center">
                              <CheckCircle className="w-4 h-4 mr-1" />
                              Implementation Steps
                            </h5>
                            <div className="space-y-2">
                              {fix.steps.map((step, stepIndex) => (
                                <motion.div
                                  key={stepIndex}
                                  initial={{ opacity: 0, x: -10 }}
                                  animate={{ opacity: 1, x: 0 }}
                                  transition={{ delay: stepIndex * 0.05 }}
                                  className="flex items-start space-x-3 p-2 rounded-lg hover:bg-zinc-700/20 transition-colors group"
                                >
                                  <div className="w-6 h-6 bg-gradient-to-r from-purple-500 to-primary-500 rounded-full flex items-center justify-center text-white text-xs font-medium flex-shrink-0">
                                    {stepIndex + 1}
                                  </div>
                                  <span className="text-zinc-600 group-hover:text-zinc-800 transition-colors">
                                    {step}
                                  </span>
                                </motion.div>
                              ))}
                            </div>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-8 flex flex-col sm:flex-row gap-4"
        >
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="btn-primary flex-1"
            onClick={() => toast.success('Fix plan exported successfully!')}
          >
            Export Fix Plan
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="btn-secondary flex-1"
            onClick={() => toast.success('Fix plan shared with team!')}
          >
            Share with Team
          </motion.button>
        </motion.div>
      </div>
    </div>
  )
}

export default FixPlan

