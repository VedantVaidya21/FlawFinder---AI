import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  AlertTriangle, 
  TrendingUp, 
  Users, 
  FileText, 
  Clock,
  ChevronRight,
  Zap,
  Target,
  Activity
} from 'lucide-react'
import BinaryBitsAnimation from '../components/BinaryBitsAnimation'
import { 
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js'
import { Line, Bar, Doughnut } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

// Mock data for demonstration
const mockFlaws = [
  { id: 1, title: 'Inefficient approval process', severity: 'High', department: 'HR', impact: 85 },
  { id: 2, title: 'Duplicate data entry', severity: 'Medium', department: 'Finance', impact: 65 },
  { id: 3, title: 'Manual inventory tracking', severity: 'High', department: 'Operations', impact: 90 },
  { id: 4, title: 'Outdated communication tools', severity: 'Low', department: 'IT', impact: 40 },
  { id: 5, title: 'Inconsistent reporting format', severity: 'Medium', department: 'Analytics', impact: 55 },
]

const Dashboard = () => {
  const [brutalityScore, setBrutalityScore] = useState(0)
  const [animatedScore, setAnimatedScore] = useState(0)

  useEffect(() => {
    // Simulate loading brutality score
    const targetScore = 73
    setBrutalityScore(targetScore)
    
    // Animate score counter
    const interval = setInterval(() => {
      setAnimatedScore(prev => {
        if (prev < targetScore) {
          return prev + 1
        }
        clearInterval(interval)
        return prev
      })
    }, 30)

    return () => clearInterval(interval)
  }, [])

  // Chart data
  const lineChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Flaws Detected',
        data: [12, 19, 8, 15, 22, 18],
        borderColor: '#a855f7',
        backgroundColor: 'rgba(168, 85, 247, 0.1)',
        tension: 0.4,
        fill: true,
      },
      {
        label: 'Flaws Fixed',
        data: [8, 15, 12, 18, 20, 24],
        borderColor: '#06b6d4',
        backgroundColor: 'rgba(6, 182, 212, 0.1)',
        tension: 0.4,
        fill: true,
      },
    ],
  }

  const barChartData = {
    labels: ['HR', 'Finance', 'Operations', 'IT', 'Marketing'],
    datasets: [
      {
        label: 'Flaws by Department',
        data: [5, 8, 12, 3, 7],
        backgroundColor: [
          'rgba(168, 85, 247, 0.8)',
          'rgba(6, 182, 212, 0.8)',
          'rgba(16, 185, 129, 0.8)',
          'rgba(245, 101, 101, 0.8)',
          'rgba(251, 191, 36, 0.8)',
        ],
        borderColor: [
          '#a855f7',
          '#06b6d4',
          '#10b981',
          '#f56565',
          '#fbbf24',
        ],
        borderWidth: 1,
      },
    ],
  }

  const doughnutData = {
    labels: ['Critical', 'High', 'Medium', 'Low'],
    datasets: [
      {
        data: [3, 8, 12, 7],
        backgroundColor: [
          '#ef4444',
          '#f97316',
          '#eab308',
          '#22c55e',
        ],
        borderWidth: 0,
      },
    ],
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#d4d4d8',
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: '#a1a1aa',
        },
        grid: {
          color: 'rgba(161, 161, 170, 0.1)',
        },
      },
      y: {
        ticks: {
          color: '#a1a1aa',
        },
        grid: {
          color: 'rgba(161, 161, 170, 0.1)',
        },
      },
    },
  }

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#d4d4d8',
          usePointStyle: true,
          padding: 20,
        },
      },
    },
  }

  return (
    <div className="min-h-screen bg-zinc-900 py-8 relative overflow-hidden">
      {/* Animated Binary Bits Background */}
      <div className="absolute inset-0 z-0">
        <BinaryBitsAnimation density={30} />
      </div>
      
      {/* Main Content */}
      <div className="relative z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold glow-text mb-2">Dashboard</h1>
          <p className="text-zinc-1000">Monitor your workflow health and operational flaws</p>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Brutality Score */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="glass-dark p-6 rounded-2xl border border-zinc-700/30 card-hover"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Target className="w-5 h-5 text-red-400" />
                <h3 className="text-sm font-medium text-zinc-600">Brutality Score</h3>
              </div>
            </div>
            <div className="relative">
              <div className="flex items-center justify-center">
                <div className="relative w-24 h-24">
                  <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 36 36">
                    <path
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none"
                      stroke="#27272a"
                      strokeWidth="2"
                    />
                    <motion.path
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none"
                      stroke="#ef4444"
                      strokeWidth="2"
                      strokeDasharray={`${animatedScore}, 100`}
                      strokeLinecap="round"
                      initial={{ strokeDasharray: "0, 100" }}
                      animate={{ strokeDasharray: `${animatedScore}, 100` }}
                      transition={{ duration: 2, ease: "easeInOut" }}
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <motion.span
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.5 }}
                      className="text-2xl font-bold text-red-400"
                    >
                      {animatedScore}
                    </motion.span>
                  </div>
                </div>
              </div>
              <p className="text-xs text-zinc-1000 text-center mt-2">Critical inefficiencies detected</p>
            </div>
          </motion.div>

          {/* Total Flaws */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="glass-dark p-6 rounded-2xl border border-zinc-700/30 card-hover"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <AlertTriangle className="w-5 h-5 text-orange-400" />
                <h3 className="text-sm font-medium text-zinc-600">Total Flaws</h3>
              </div>
              <span className="text-xs bg-orange-500/20 text-orange-400 px-2 py-1 rounded-full">+12%</span>
            </div>
            <div className="flex items-end space-x-2">
              <span className="text-3xl font-bold text-zinc-100">42</span>
              <span className="text-sm text-zinc-1000 mb-1">detected</span>
            </div>
          </motion.div>

          {/* Active Departments */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
            className="glass-dark p-6 rounded-2xl border border-zinc-700/30 card-hover"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Users className="w-5 h-5 text-purple-400" />
                <h3 className="text-sm font-medium text-zinc-600">Departments</h3>
              </div>
              <span className="text-xs bg-purple-500/20 text-purple-400 px-2 py-1 rounded-full">5 active</span>
            </div>
            <div className="flex items-end space-x-2">
              <span className="text-3xl font-bold text-zinc-100">8</span>
              <span className="text-sm text-zinc-1000 mb-1">analyzed</span>
            </div>
          </motion.div>

          {/* Processing Time */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
            className="glass-dark p-6 rounded-2xl border border-zinc-700/30 card-hover"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Clock className="w-5 h-5 text-primary-400" />
                <h3 className="text-sm font-medium text-zinc-600">Avg. Fix Time</h3>
              </div>
              <span className="text-xs bg-primary-500/20 text-primary-400 px-2 py-1 rounded-full">-8%</span>
            </div>
            <div className="flex items-end space-x-2">
              <span className="text-3xl font-bold text-zinc-100">3.2</span>
              <span className="text-sm text-zinc-1000 mb-1">days</span>
            </div>
          </motion.div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Line Chart */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="glass-dark p-6 rounded-2xl border border-zinc-700/30"
          >
            <h3 className="text-lg font-semibold text-zinc-100 mb-4 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-purple-400" />
              Flaw Detection Trends
            </h3>
            <div className="h-64">
              <Line data={lineChartData} options={chartOptions} />
            </div>
          </motion.div>

          {/* Doughnut Chart */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="glass-dark p-6 rounded-2xl border border-zinc-700/30"
          >
            <h3 className="text-lg font-semibold text-zinc-100 mb-4 flex items-center">
              <Activity className="w-5 h-5 mr-2 text-primary-400" />
              Severity Distribution
            </h3>
            <div className="h-64">
              <Doughnut data={doughnutData} options={doughnutOptions} />
            </div>
          </motion.div>
        </div>

        {/* Bar Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="glass-dark p-6 rounded-2xl border border-zinc-700/30 mb-8"
        >
          <h3 className="text-lg font-semibold text-zinc-100 mb-4 flex items-center">
            <FileText className="w-5 h-5 mr-2 text-green-400" />
            Flaws by Department
          </h3>
          <div className="h-64">
            <Bar data={barChartData} options={chartOptions} />
          </div>
        </motion.div>

        {/* Recent Flaws */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="glass-dark p-6 rounded-2xl border border-zinc-700/30"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-zinc-100 flex items-center">
              <Zap className="w-5 h-5 mr-2 text-yellow-400" />
              Recent Flaws Detected
            </h3>
            <button className="text-purple-400 hover:text-purple-300 text-sm font-medium">
              View All
            </button>
          </div>
          
          <div className="space-y-4">
            {mockFlaws.map((flaw, index) => (
              <motion.div
                key={flaw.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.9 + index * 0.1 }}
                className="flex items-center justify-between p-4 bg-zinc-800/50 rounded-xl border border-zinc-700/30 hover:border-purple-500/30 transition-all duration-300 group cursor-pointer"
              >
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full ${
                      flaw.severity === 'High' ? 'bg-red-500' :
                      flaw.severity === 'Medium' ? 'bg-yellow-500' : 'bg-green-500'
                    }`} />
                    <h4 className="text-zinc-100 font-medium">{flaw.title}</h4>
                    <span className="text-xs text-zinc-1000 bg-zinc-700/50 px-2 py-1 rounded-full">
                      {flaw.department}
                    </span>
                  </div>
                  <div className="flex items-center mt-2">
                    <div className="w-32 bg-zinc-700 rounded-full h-2 mr-3">
                      <div 
                        className="bg-gradient-to-r from-purple-500 to-primary-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${flaw.impact}%` }}
                      />
                    </div>
                    <span className="text-sm text-zinc-1000">{flaw.impact}% impact</span>
                  </div>
                </div>
                <ChevronRight className="w-5 h-5 text-zinc-1000 group-hover:text-purple-400 transition-colors" />
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
      </div>
    </div>
  )
}

export default Dashboard

