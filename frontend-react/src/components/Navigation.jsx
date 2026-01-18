import { motion } from 'framer-motion'

const Navigation = ({ tabs, activeTab, setActiveTab }) => {
  return (
    <motion.nav
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6"
    >
      <div className="glass rounded-2xl p-2 flex space-x-2">
        {tabs.map((tab, index) => {
          const Icon = tab.icon
          const isActive = activeTab === tab.id
          
          return (
            <motion.button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                relative flex items-center space-x-2 px-6 py-3 rounded-xl
                font-medium transition-all duration-300 flex-1
                ${isActive 
                  ? 'text-white' 
                  : 'text-slate-400 hover:text-slate-200'
                }
              `}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              {isActive && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-700 rounded-xl"
                  transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                />
              )}
              <Icon className={`w-5 h-5 relative z-10 ${isActive ? 'text-white' : ''}`} />
              <span className="relative z-10">{tab.name}</span>
            </motion.button>
          )
        })}
      </div>
    </motion.nav>
  )
}

export default Navigation
