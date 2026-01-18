import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

const Analytics = () => {
  const [trends, setTrends] = useState([])
  const [suppliers, setSuppliers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const [trendsRes, suppliersRes] = await Promise.all([
        axios.get('/api/price-trends'),
        axios.get('/api/suppliers')
      ])
      setTrends(trendsRes.data)
      setSuppliers(suppliersRes.data.slice(0, 8))
    } catch (error) {
      console.error('Error fetching analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#fee140', '#30cfd0']

  const trendIcons = {
    up: TrendingUp,
    down: TrendingDown,
    stable: Minus
  }

  if (loading) {
    return (
      <div className="space-y-6">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="glass rounded-2xl p-6 shimmer h-96" />
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
        <h2 className="text-2xl font-bold">Cost Analytics</h2>
        <p className="text-slate-400 mt-1">Comprehensive analysis of pricing trends and supplier performance</p>
      </motion.div>

      {/* Price Trends */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass rounded-2xl p-6"
      >
        <h3 className="text-xl font-bold mb-6">Price Trends by Item</h3>
        <div className="w-full overflow-x-auto">
          <ResponsiveContainer width="100%" height={450}>
            <BarChart 
              data={trends} 
              margin={{ top: 20, right: 30, left: 60, bottom: 100 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis 
                dataKey="item_name" 
                stroke="#94a3b8"
                angle={-45}
                textAnchor="end"
                height={120}
                interval={0}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                stroke="#94a3b8"
                tick={{ fontSize: 12 }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #475569',
                  borderRadius: '8px',
                  color: '#e2e8f0'
                }}
                formatter={(value) => [`₹${Number(value).toFixed(2)}`, '']}
              />
              <Legend 
                verticalAlign="bottom" 
                align="center"
                wrapperStyle={{ paddingTop: '30px', paddingBottom: '10px' }} 
              />
              <Bar dataKey="avg_price" fill="#667eea" name="Avg Price" radius={[8, 8, 0, 0]} />
              <Bar dataKey="min_price" fill="#10b981" name="Min Price" radius={[8, 8, 0, 0]} />
              <Bar dataKey="max_price" fill="#ef4444" name="Max Price" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* Trend Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {trends.slice(0, 6).map((trend, index) => {
          const TrendIcon = trendIcons[trend.trend_direction] || Minus
          const trendColor = 
            trend.trend_direction === 'up' ? 'text-red-400' :
            trend.trend_direction === 'down' ? 'text-green-400' :
            'text-slate-400'

          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + index * 0.05 }}
              whileHover={{ scale: 1.03 }}
              className="glass rounded-2xl p-6 card-hover"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h4 className="font-semibold text-white truncate">{trend.item_name}</h4>
                  <p className="text-sm text-slate-400 mt-1">Price Analysis</p>
                </div>
                <div className={`p-2 rounded-lg ${trendColor} bg-slate-800`}>
                  <TrendIcon className="w-5 h-5" />
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Avg Price</span>
                  <span className="font-semibold text-white">₹{trend.avg_price?.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Range</span>
                  <span className="font-semibold text-white">
                    ₹{trend.min_price?.toFixed(2)} - ₹{trend.max_price?.toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Variance</span>
                  <span className="font-semibold text-white">₹{trend.price_variance?.toFixed(2)}</span>
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Supplier Performance */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="glass rounded-2xl p-6"
      >
        <h3 className="text-xl font-bold mb-6">Supplier Performance</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="flex items-center justify-center">
            <ResponsiveContainer width="100%" height={350}>
              <PieChart>
                <Pie
                  data={suppliers}
                  dataKey="item_count"
                  nameKey="supplier"
                  cx="50%"
                  cy="50%"
                  outerRadius={120}
                  label={(entry) => `${entry.supplier.substring(0, 15)}${entry.supplier.length > 15 ? '...' : ''}`}
                  labelLine={true}
                >
                  {suppliers.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1e293b', 
                    border: '1px solid #475569',
                    borderRadius: '8px',
                    color: '#e2e8f0'
                  }}
                  formatter={(value, name) => [`${value} items`, name]}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="space-y-3 flex flex-col justify-center">
            {suppliers.map((supplier, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + index * 0.05 }}
                className="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl hover:bg-slate-800/50 transition-colors"
              >
                <div className="flex items-center space-x-3 flex-1 min-w-0">
                  <div 
                    className="w-4 h-4 rounded-full flex-shrink-0"
                    style={{ backgroundColor: COLORS[index % COLORS.length] }}
                  />
                  <span className="font-medium text-white truncate">{supplier.supplier}</span>
                </div>
                <div className="text-right flex-shrink-0 ml-4">
                  <div className="font-semibold text-white">{supplier.item_count} items</div>
                  <div className="text-sm text-slate-400">Avg: ₹{supplier.avg_price?.toFixed(2)}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default Analytics
