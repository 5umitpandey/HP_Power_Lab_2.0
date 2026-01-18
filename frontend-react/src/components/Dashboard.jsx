import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import { 
  Package, IndianRupee, Users, TrendingUp, 
  AlertTriangle, Activity, ArrowUp, ArrowDown,
  FileText, BarChart3, Download 
} from 'lucide-react'

const Dashboard = ({ setActiveTab }) => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/dashboard/stats')
      setStats(response.data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = stats ? [
    {
      title: 'Total Items',
      value: stats.total_items?.toLocaleString() || '0',
      icon: Package,
      color: 'from-blue-500 to-cyan-500',
      change: '+12.5%',
      trending: 'up'
    },
    {
      title: 'Suppliers',
      value: stats.total_suppliers?.toLocaleString() || '0',
      icon: Users,
      color: 'from-purple-500 to-pink-500',
      change: '+3.2%',
      trending: 'up'
    },
    {
      title: 'Avg Unit Price',
      value: `₹${stats.avg_unit_price?.toFixed(2) || '0'}`,
      icon: IndianRupee,
      color: 'from-green-500 to-emerald-500',
      change: '-2.1%',
      trending: 'down'
    },
    {
      title: 'Avg Confidence',
      value: `${(stats.avg_confidence * 100)?.toFixed(1) || '0'}%`,
      icon: Activity,
      color: 'from-orange-500 to-red-500',
      change: '+5.8%',
      trending: 'up'
    },
    {
      title: 'Anomalies',
      value: stats.items_with_anomalies?.toLocaleString() || '0',
      icon: AlertTriangle,
      color: 'from-red-500 to-rose-500',
      change: '-8.3%',
      trending: 'down'
    },
    {
      title: 'Categories',
      value: stats.total_categories?.toLocaleString() || '0',
      icon: TrendingUp,
      color: 'from-indigo-500 to-purple-500',
      change: '+1.5%',
      trending: 'up'
    },
  ] : []

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="glass rounded-2xl p-6 shimmer h-40" />
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-2xl p-8"
      >
        <h2 className="text-3xl font-bold mb-2">Welcome Back! 👋</h2>
        <p className="text-slate-400">
          Here's what's happening with your procurement data today.
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon
          const TrendIcon = stat.trending === 'up' ? ArrowUp : ArrowDown
          
          return (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.03, y: -5 }}
              className="glass rounded-2xl p-6 card-hover cursor-pointer"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${stat.color} flex items-center justify-center shadow-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <div className={`flex items-center space-x-1 text-sm font-semibold ${
                  stat.trending === 'up' ? 'text-green-400' : 'text-red-400'
                }`}>
                  <TrendIcon className="w-4 h-4" />
                  <span>{stat.change}</span>
                </div>
              </div>
              
              <h3 className="text-slate-400 text-sm font-medium mb-1">{stat.title}</h3>
              <p className="text-3xl font-bold text-white">{stat.value}</p>
              
              {/* Animated progress bar */}
              <motion.div
                className="mt-4 h-1 bg-slate-700 rounded-full overflow-hidden"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: index * 0.1 + 0.3 }}
              >
                <motion.div
                  className={`h-full bg-gradient-to-r ${stat.color}`}
                  initial={{ width: 0 }}
                  animate={{ width: '75%' }}
                  transition={{ duration: 1, delay: index * 0.1 + 0.5, ease: 'easeOut' }}
                />
              </motion.div>
            </motion.div>
          )
        })}
      </div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="glass rounded-2xl p-6"
      >
        <h3 className="text-xl font-bold mb-4">Quick Actions</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setActiveTab('items')}
            className="p-4 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 text-white font-semibold shadow-lg hover:shadow-xl transition-shadow flex flex-col items-center space-y-2"
          >
            <Package className="w-6 h-6" />
            <span>View All Items</span>
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setActiveTab('analytics')}
            className="p-4 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 text-white font-semibold shadow-lg hover:shadow-xl transition-shadow flex flex-col items-center space-y-2"
          >
            <BarChart3 className="w-6 h-6" />
            <span>Analytics Report</span>
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setActiveTab('anomalies')}
            className="p-4 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 text-white font-semibold shadow-lg hover:shadow-xl transition-shadow flex flex-col items-center space-y-2"
          >
            <AlertTriangle className="w-6 h-6" />
            <span>Check Anomalies</span>
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={async () => {
              try {
                const response = await axios.get('/api/items', { params: { per_page: 10000 } })
                const dataStr = JSON.stringify(response.data.items, null, 2)
                const dataBlob = new Blob([dataStr], { type: 'application/json' })
                const url = URL.createObjectURL(dataBlob)
                const link = document.createElement('a')
                link.href = url
                link.download = `cost-database-export-${new Date().toISOString().split('T')[0]}.json`
                document.body.appendChild(link)
                link.click()
                document.body.removeChild(link)
                URL.revokeObjectURL(url)
              } catch (error) {
                console.error('Export failed:', error)
                alert('Failed to export data. Please try again.')
              }
            }}
            className="p-4 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 text-white font-semibold shadow-lg hover:shadow-xl transition-shadow flex flex-col items-center space-y-2"
          >
            <Download className="w-6 h-6" />
            <span>Export Data</span>
          </motion.button>
        </div>
      </motion.div>
    </div>
  )
}

export default Dashboard
