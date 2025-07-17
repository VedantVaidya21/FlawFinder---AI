import { motion } from 'framer-motion'
import { Download, FileText, Printer, TrendingUp, Users, AlertCircle, CheckCircle, BarChart3 } from 'lucide-react'
import { useState } from 'react'
import toast from 'react-hot-toast'

const pagination = [
  { name: 'Overview', current: true },
  { name: 'HR', current: false },
  { name: 'Finance', current: false },
  { name: 'Operations', current: false },
  { name: 'IT', current: false },
  { name: 'Marketing', current: false },
]

const CEOReport = () => {
  const [tabs, setTabs] = useState(pagination)

  const toggleTab = (index) => {
    setTabs(
      tabs.map((tab, i) => {
        if (i === index) {
          return { ...tab, current: true }
        }
        return { ...tab, current: false }
      })
    )
  }

  const handleExportPDF = () => {
    toast.success('Report exported to PDF successfully!')
  }

  const handlePrint = () => {
    toast.success('Report sent to printer!')
  }

  const currentTab = tabs.find(tab => tab.current)

  return (
    <div className="min-h-screen bg-zinc-900 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold glow-text mb-2">CEO Report</h1>
          <p className="text-zinc-1000">Comprehensive analysis and insights for executive decision-making</p>
        </motion.div>

        {/* Navigation Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 border-b border-zinc-700/30"
        >
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            {tabs.map((tab, index) => (
              <motion.a
                key={tab.name}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => toggleTab(index)}
                className={`${tab.current ? 'border-purple-500 text-purple-400' : 'border-transparent text-zinc-1000 hover:text-zinc-800 hover:border-zinc-700'} whitespace-nowrap pb-2 px-1 border-b-2 font-medium text-sm cursor-pointer transition-all duration-200`}
              >
                {tab.name}
              </motion.a>
            ))}
          </nav>
        </motion.div>

        {/* Report Viewer */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-dark p-8 rounded-2xl border border-zinc-700/30 shadow-glass"
        >
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-zinc-100 flex items-center">
              <BarChart3 className="w-6 h-6 mr-2 text-purple-400" />
              {currentTab.name} Report
            </h2>
            <div className="flex space-x-3">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-primary flex items-center"
                onClick={handleExportPDF}
              >
                <Download className="w-4 h-4 mr-2" />
                Export PDF
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-secondary flex items-center"
                onClick={handlePrint}
              >
                <Printer className="w-4 h-4 mr-2" />
                Print
              </motion.button>
            </div>
          </div>
          
          {/* Report Content */}
          <div className="space-y-6">
            {/* Executive Summary */}
            <div className="bg-zinc-800/30 p-6 rounded-xl border border-zinc-700/20">
              <h3 className="text-lg font-semibold text-zinc-100 mb-4 flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-green-400" />
                Executive Summary
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-zinc-700/20 rounded-lg">
                  <div className="text-2xl font-bold text-purple-400 mb-1">73</div>
                  <div className="text-sm text-zinc-1000">Brutality Score</div>
                </div>
                <div className="text-center p-4 bg-zinc-700/20 rounded-lg">
                  <div className="text-2xl font-bold text-orange-400 mb-1">42</div>
                  <div className="text-sm text-zinc-1000">Total Flaws</div>
                </div>
                <div className="text-center p-4 bg-zinc-700/20 rounded-lg">
                  <div className="text-2xl font-bold text-green-400 mb-1">18</div>
                  <div className="text-sm text-zinc-1000">Fixes Implemented</div>
                </div>
              </div>
            </div>

            {/* Key Findings */}
            <div className="bg-zinc-800/30 p-6 rounded-xl border border-zinc-700/20">
              <h3 className="text-lg font-semibold text-zinc-100 mb-4 flex items-center">
                <AlertCircle className="w-5 h-5 mr-2 text-yellow-400" />
                Key Findings
              </h3>
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                  <div>
                    <p className="text-zinc-600 font-medium">Critical inefficiencies in approval processes</p>
                    <p className="text-sm text-zinc-1000">Average approval time: 7.2 days (industry standard: 2.1 days)</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2 flex-shrink-0"></div>
                  <div>
                    <p className="text-zinc-600 font-medium">Manual data entry causing delays</p>
                    <p className="text-sm text-zinc-1000">38% of workflows involve duplicate data entry</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                  <div>
                    <p className="text-zinc-600 font-medium">Strong performance in IT automation</p>
                    <p className="text-sm text-zinc-1000">92% of IT processes are automated</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Recommendations */}
            <div className="bg-zinc-800/30 p-6 rounded-xl border border-zinc-700/20">
              <h3 className="text-lg font-semibold text-zinc-100 mb-4 flex items-center">
                <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                Strategic Recommendations
              </h3>
              <div className="space-y-4">
                <div className="flex items-start space-x-3 p-3 bg-zinc-700/20 rounded-lg">
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-primary-500 rounded-full flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
                    1
                  </div>
                  <div>
                    <p className="text-zinc-600 font-medium">Implement workflow automation platform</p>
                    <p className="text-sm text-zinc-1000">Estimated ROI: 340% within 12 months</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3 p-3 bg-zinc-700/20 rounded-lg">
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-primary-500 rounded-full flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
                    2
                  </div>
                  <div>
                    <p className="text-zinc-600 font-medium">Integrate systems to eliminate duplicate data entry</p>
                    <p className="text-sm text-zinc-1000">Potential time savings: 15-20 hours per week per employee</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3 p-3 bg-zinc-700/20 rounded-lg">
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-primary-500 rounded-full flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
                    3
                  </div>
                  <div>
                    <p className="text-zinc-600 font-medium">Establish continuous improvement culture</p>
                    <p className="text-sm text-zinc-1000">Regular workflow audits and optimization cycles</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Department Specific Data */}
            {currentTab.name !== 'Overview' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-zinc-800/30 p-6 rounded-xl border border-zinc-700/20"
              >
                <h3 className="text-lg font-semibold text-zinc-100 mb-4 flex items-center">
                  <Users className="w-5 h-5 mr-2 text-primary-400" />
                  {currentTab.name} Department Analysis
                </h3>
                <div className="text-center py-12">
                  <div className="text-zinc-1000 mb-4">
                    <BarChart3 className="w-16 h-16 mx-auto mb-4 opacity-50" />
                    <p>Detailed {currentTab.name} analysis and metrics will be displayed here.</p>
                    <p className="text-sm mt-2">This would include department-specific KPIs, flaw patterns, and tailored recommendations.</p>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default CEOReport


