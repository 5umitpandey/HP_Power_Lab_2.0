import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Dashboard from './components/Dashboard'
import ItemsTable from './components/ItemsTable'
import Analytics from './components/Analytics'
import Anomalies from './components/Anomalies'
import Upload from './components/Upload'
import Navigation from './components/Navigation'
import BackgroundAnimation from './components/BackgroundAnimation'
import { Database, TrendingUp, AlertCircle, BarChart3, Upload as UploadIcon } from 'lucide-react'
import hpLogo from '../assets/hp logo.png'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate initial loading
    setTimeout(() => setIsLoading(false), 1000)
  }, [])

  const tabs = [
    { id: 'upload', name: 'Upload', icon: UploadIcon },
    { id: 'dashboard', name: 'Dashboard', icon: Database },
    { id: 'items', name: 'Items', icon: BarChart3 },
    { id: 'analytics', name: 'Analytics', icon: TrendingUp },
    { id: 'anomalies', name: 'Anomalies', icon: AlertCircle },
  ]

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard setActiveTab={setActiveTab} />
      case 'items':
        return <ItemsTable />
      case 'analytics':
        return <Analytics />
      case 'anomalies':
        return <Anomalies />
      case 'upload':
        return <Upload />
      default:
        return <Dashboard setActiveTab={setActiveTab} />
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <BackgroundAnimation />
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="text-center z-10"
        >
          <div className="w-32 h-32 mx-auto mb-4 relative">
            <motion.img
              src={hpLogo}
              alt="HPCL Logo"
              className="w-full h-full object-contain"
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
            />
          </div>
          <h2 className="text-2xl font-bold gradient-text">Loading...</h2>
          <p className="text-slate-400 mt-2">HPCL Intelligent Cost Database</p>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="min-h-screen relative overflow-hidden">
      <BackgroundAnimation />
      
      <div className="relative z-10">
        {/* Header */}
        <motion.header
          initial={{ y: -100 }}
          animate={{ y: 0 }}
          transition={{ duration: 0.5 }}
          className="glass border-b border-slate-700/50"
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <motion.div
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setActiveTab('upload')}
                className="flex items-center space-x-3 cursor-pointer"
              >
                <img 
                  src={hpLogo} 
                  alt="HPCL Logo" 
                  className="w-14 h-14 object-contain"
                />
                <div>
                  <h1 className="text-2xl font-bold text-white">
                    HPCL Intelligent Cost Database
                  </h1>
                  <p className="text-sm text-slate-400">AI-Powered Procurement Analytics</p>
                </div>
              </motion.div>
              
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="flex items-center space-x-4"
              >
                <div className="px-4 py-2 rounded-lg glass">
                  <span className="text-sm text-slate-300">
                    {new Date().toLocaleDateString('en-US', { 
                      weekday: 'short', 
                      year: 'numeric', 
                      month: 'short', 
                      day: 'numeric' 
                    })}
                  </span>
                </div>
              </motion.div>
            </div>
          </div>
        </motion.header>

        {/* Navigation */}
        <Navigation tabs={tabs} activeTab={activeTab} setActiveTab={setActiveTab} />

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {renderContent()}
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  )
}

export default App
