import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import { AlertTriangle, AlertCircle, Info, CheckCircle } from 'lucide-react'

const Anomalies = () => {
  const [anomalies, setAnomalies] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    fetchAnomalies()
  }, [])

  const fetchAnomalies = async () => {
    try {
      const response = await axios.get('/api/anomalies')
      setAnomalies(response.data)
    } catch (error) {
      console.error('Error fetching anomalies:', error)
    } finally {
      setLoading(false)
    }
  }

  const getSeverityConfig = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
        return {
          icon: AlertTriangle,
          color: 'from-red-500 to-rose-500',
          bg: 'bg-red-500/10',
          border: 'border-red-500/30',
          text: 'text-red-400'
        }
      case 'medium':
        return {
          icon: AlertCircle,
          color: 'from-yellow-500 to-orange-500',
          bg: 'bg-yellow-500/10',
          border: 'border-yellow-500/30',
          text: 'text-yellow-400'
        }
      case 'low':
        return {
          icon: Info,
          color: 'from-blue-500 to-cyan-500',
          bg: 'bg-blue-500/10',
          border: 'border-blue-500/30',
          text: 'text-blue-400'
        }
      default:
        return {
          icon: CheckCircle,
          color: 'from-green-500 to-emerald-500',
          bg: 'bg-green-500/10',
          border: 'border-green-500/30',
          text: 'text-green-400'
        }
    }
  }

  const filteredAnomalies = filter === 'all' 
    ? anomalies 
    : anomalies.filter(a => a.anomaly_type?.toLowerCase() === filter.toLowerCase())

  if (loading) {
    return (
      <div className="space-y-6">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="glass rounded-2xl p-6 shimmer h-32" />
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-2xl p-6"
      >
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <div>
            <h2 className="text-2xl font-bold">Price Anomalies</h2>
            <p className="text-slate-400 mt-1">
              Detected {anomalies.length} potential pricing issues
            </p>
          </div>

          {/* Filter Buttons */}
          <div className="flex space-x-2">
            {['all', 'high', 'medium', 'low'].map((level) => (
              <motion.button
                key={level}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setFilter(level)}
                className={`px-4 py-2 rounded-lg font-medium capitalize transition-all ${
                  filter === level
                    ? 'bg-gradient-to-r from-blue-600 to-indigo-700 text-white'
                    : 'bg-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                {level}
              </motion.button>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Anomaly Cards */}
      <div className="space-y-4">
        {filteredAnomalies.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="glass rounded-2xl p-12 text-center"
          >
            <CheckCircle className="w-16 h-16 mx-auto text-green-400 mb-4" />
            <h3 className="text-xl font-bold mb-2">No Anomalies Found</h3>
            <p className="text-slate-400">
              {filter === 'all' 
                ? 'Great! No pricing anomalies detected in your data.'
                : `No ${filter} severity anomalies found.`}
            </p>
          </motion.div>
        ) : (
          filteredAnomalies.map((anomaly, index) => {
            const config = getSeverityConfig(anomaly.anomaly_severity || anomaly.severity)
            const Icon = config.icon

            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                whileHover={{ scale: 1.01 }}
                className={`glass rounded-2xl p-6 border-l-4 ${config.border} card-hover`}
              >
                <div className="flex items-start space-x-4">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${config.color} flex items-center justify-center flex-shrink-0`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>

                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="text-lg font-semibold text-white">
                          {anomaly.canonical_item_name || anomaly.item_name || 'Unknown Item'}
                        </h3>
                        <p className="text-sm text-slate-400 mt-1">
                          {anomaly.supplier_name || 'Unknown Supplier'}
                        </p>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${config.bg} ${config.text} capitalize`}>
                        {anomaly.anomaly_severity || anomaly.severity || 'Unknown'}
                      </span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                      <div className={`p-3 rounded-lg ${config.bg}`}>
                        <p className="text-xs text-slate-400 mb-1">Current Price</p>
                        <p className="text-lg font-semibold text-white">
                          ₹{anomaly.unit_price?.toFixed(2) || '0.00'}
                        </p>
                      </div>
                      <div className={`p-3 rounded-lg ${config.bg}`}>
                        <p className="text-xs text-slate-400 mb-1">Expected Range</p>
                        <p className="text-lg font-semibold text-white">
                          ₹{anomaly.expected_min?.toFixed(2) || '0.00'} - ₹{anomaly.expected_max?.toFixed(2) || '0.00'}
                        </p>
                      </div>
                      <div className={`p-3 rounded-lg ${config.bg}`}>
                        <p className="text-xs text-slate-400 mb-1">Deviation</p>
                        <p className={`text-lg font-semibold ${config.text}`}>
                          {anomaly.deviation_percentage?.toFixed(1) || '0.0'}%
                        </p>
                      </div>
                    </div>

                    <div className={`p-4 rounded-lg ${config.bg} border ${config.border}`}>
                      <p className="text-sm font-medium text-slate-300 mb-2">
                        🔍 Detection Details:
                      </p>
                      <p className="text-sm text-slate-400">
                        {anomaly.description || anomaly.reason || 
                          `This item's price deviates significantly from the expected range, indicating a potential pricing anomaly.`}
                      </p>
                    </div>
                  </div>
                </div>
              </motion.div>
            )
          })
        )}
      </div>
    </div>
  )
}

export default Anomalies
