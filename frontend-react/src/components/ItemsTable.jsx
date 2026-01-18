import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import { Search, Filter, ChevronLeft, ChevronRight } from 'lucide-react'

const ItemsTable = () => {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [search, setSearch] = useState('')

  useEffect(() => {
    fetchItems()
  }, [page, search])

  const fetchItems = async () => {
    setLoading(true)
    try {
      const response = await axios.get('/api/items', {
        params: { page, per_page: 15, search }
      })
      setItems(response.data.items)
      setTotalPages(response.data.pages)
    } catch (error) {
      console.error('Error fetching items:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    setSearch(e.target.value)
    setPage(1)
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
            <h2 className="text-2xl font-bold">Standardized Items</h2>
            <p className="text-slate-400 mt-1">Browse and search procurement items</p>
          </div>
          
          {/* Search Bar */}
          <div className="relative w-full md:w-96">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search items or suppliers..."
              value={search}
              onChange={handleSearch}
              className="w-full pl-12 pr-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl 
                       text-white placeholder-slate-400 focus:outline-none focus:ring-2 
                       focus:ring-primary-500 transition-all"
            />
          </div>
        </div>
      </motion.div>

      {/* Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass rounded-2xl overflow-hidden"
      >
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-800/50 border-b border-slate-700">
              <tr>
                {['Item Name', 'Supplier', 'Unit Price', 'Confidence', 'Category'].map((header) => (
                  <th key={header} className="px-6 py-4 text-left text-sm font-semibold text-slate-300">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <AnimatePresence mode="wait">
                {loading ? (
                  [...Array(10)].map((_, i) => (
                    <tr key={`skeleton-${i}`} className="border-b border-slate-700/50">
                      {[...Array(5)].map((_, j) => (
                        <td key={`skeleton-${i}-${j}`} className="px-6 py-4">
                          <div className="h-6 bg-slate-700 rounded shimmer" />
                        </td>
                      ))}
                    </tr>
                  ))
                ) : (
                  items.map((item, index) => (
                    <motion.tr
                      key={`${item.po_id || item.item_code}-${index}`}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 20 }}
                      transition={{ delay: index * 0.05 }}
                      className="border-b border-slate-700/50 hover:bg-slate-800/30 transition-colors"
                    >
                      <td className="px-6 py-4">
                        <div className="font-medium text-white">
                          {item.canonical_item_name || 'N/A'}
                        </div>
                        <div className="text-sm text-slate-400 mt-1">
                          {item.item_code || 'No code'}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-slate-300">
                        {item.supplier_name || 'N/A'}
                      </td>
                      <td className="px-6 py-4">
                        <span className="text-green-400 font-semibold">
                          ₹{item.unit_price?.toFixed(2) || '0.00'}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center space-x-2">
                          <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${(item.standardization_confidence || 0) * 100}%` }}
                              transition={{ duration: 0.8, delay: index * 0.05 }}
                              className={`h-full rounded-full ${
                                item.standardization_confidence > 0.8
                                  ? 'bg-green-500'
                                  : item.standardization_confidence > 0.6
                                  ? 'bg-yellow-500'
                                  : 'bg-red-500'
                              }`}
                            />
                          </div>
                          <span className="text-sm text-slate-400 w-12">
                            {((item.standardization_confidence || 0) * 100).toFixed(0)}%
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span className="px-3 py-1 rounded-full text-xs font-semibold bg-primary-500/20 text-primary-300">
                          {item.category || 'Uncategorized'}
                        </span>
                      </td>
                    </motion.tr>
                  ))
                )}
              </AnimatePresence>
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between px-6 py-4 bg-slate-800/30 border-t border-slate-700">
          <div className="text-sm text-slate-400">
            Page {page} of {totalPages}
          </div>
          <div className="flex space-x-2">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-4 py-2 rounded-lg bg-slate-700 text-white disabled:opacity-50 
                       disabled:cursor-not-allowed hover:bg-slate-600 transition-colors"
            >
              <ChevronLeft className="w-5 h-5" />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="px-4 py-2 rounded-lg bg-slate-700 text-white disabled:opacity-50 
                       disabled:cursor-not-allowed hover:bg-slate-600 transition-colors"
            >
              <ChevronRight className="w-5 h-5" />
            </motion.button>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default ItemsTable
