import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import { 
  Upload as UploadIcon, 
  FileText, 
  CheckCircle, 
  AlertCircle, 
  Loader, 
  Download,
  ArrowRight,
  Database,
  Zap
} from 'lucide-react'

const Upload = () => {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [processing, setProcessing] = useState(false)
  const [uploadResult, setUploadResult] = useState(null)
  const [processResult, setProcessResult] = useState(null)
  const [error, setError] = useState(null)
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.name.endsWith('.csv')) {
        setFile(droppedFile)
        setError(null)
      } else {
        setError('Please upload a CSV file')
      }
    }
  }

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0]
      if (selectedFile.name.endsWith('.csv')) {
        setFile(selectedFile)
        setError(null)
      } else {
        setError('Please upload a CSV file')
      }
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first')
      return
    }

    setUploading(true)
    setError(null)
    setUploadResult(null)
    setProcessResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      setUploadResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  const handleProcess = async () => {
    setProcessing(true)
    setError(null)

    try {
      const response = await axios.post('/api/process')
      setProcessResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error || 'Processing failed')
    } finally {
      setProcessing(false)
    }
  }

  const downloadTemplate = async () => {
    try {
      const response = await axios.get('/api/download-template', {
        responseType: 'blob'
      })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'purchase_orders_template.csv')
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      setError('Failed to download template')
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-2xl p-6"
      >
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold flex items-center space-x-3">
              <Database className="w-8 h-8 text-primary-400" />
              <span>Upload & Process Data</span>
            </h2>
            <p className="text-slate-400 mt-2">
              Upload raw purchase order data and process it through AI standardization and analytics
            </p>
          </div>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={downloadTemplate}
            className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-white transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Download Template</span>
          </motion.button>
        </div>
      </motion.div>

      {/* Upload Area */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass rounded-2xl p-8"
      >
        <h3 className="text-xl font-bold mb-6">Step 1: Upload CSV File</h3>
        
        <div
          className={`border-2 border-dashed rounded-xl p-12 text-center transition-all ${
            dragActive
              ? 'border-primary-500 bg-primary-500/10'
              : 'border-slate-600 hover:border-slate-500'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            className="hidden"
            id="file-upload"
          />
          
          <label
            htmlFor="file-upload"
            className="cursor-pointer flex flex-col items-center space-y-4"
          >
            <motion.div
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
              className="w-20 h-20 rounded-full bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center"
            >
              <UploadIcon className="w-10 h-10 text-white" />
            </motion.div>
            
            <div>
              <p className="text-lg font-semibold text-white">
                {file ? file.name : 'Drop your CSV file here or click to browse'}
              </p>
              <p className="text-sm text-slate-400 mt-2">
                Supports CSV files up to 16MB
              </p>
            </div>
          </label>

          {file && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              className="mt-6 p-4 bg-green-500/10 border border-green-500/30 rounded-lg"
            >
              <div className="flex items-center justify-center space-x-3 text-green-400">
                <FileText className="w-5 h-5" />
                <span className="font-medium">{file.name}</span>
                <span className="text-sm">({(file.size / 1024).toFixed(2)} KB)</span>
              </div>
            </motion.div>
          )}
        </div>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleUpload}
          disabled={!file || uploading}
          className="w-full mt-6 px-6 py-4 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-700 text-white font-semibold text-lg
                   disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-xl transition-all flex items-center justify-center space-x-3"
        >
          {uploading ? (
            <>
              <Loader className="w-6 h-6 animate-spin" />
              <span>Uploading...</span>
            </>
          ) : (
            <>
              <UploadIcon className="w-6 h-6" />
              <span>Upload File</span>
            </>
          )}
        </motion.button>
      </motion.div>

      {/* Upload Result */}
      <AnimatePresence>
        {uploadResult && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="glass rounded-2xl p-6 border-l-4 border-green-500"
          >
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 rounded-xl bg-green-500/20 flex items-center justify-center flex-shrink-0">
                <CheckCircle className="w-6 h-6 text-green-400" />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-white mb-2">Upload Successful!</h3>
                <div className="space-y-2 text-slate-300">
                  <p>✓ File: {uploadResult.filename}</p>
                  <p>✓ Rows: {uploadResult.rows}</p>
                  <p>✓ Columns: {uploadResult.columns?.join(', ')}</p>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Process Section */}
      <AnimatePresence>
        {uploadResult && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass rounded-2xl p-8"
          >
            <h3 className="text-xl font-bold mb-6 flex items-center space-x-3">
              <Zap className="w-6 h-6 text-yellow-400" />
              <span>Step 2: Process Data</span>
            </h3>
            
            <div className="space-y-4 mb-6">
              <div className="p-4 bg-slate-800/50 rounded-lg">
                <p className="text-slate-300">The processing pipeline will:</p>
                <ul className="mt-3 space-y-2 text-slate-400">
                  <li className="flex items-center space-x-2">
                    <ArrowRight className="w-4 h-4 text-primary-400" />
                    <span>Standardize item descriptions using AI</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <ArrowRight className="w-4 h-4 text-primary-400" />
                    <span>Generate cost analytics and trends</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <ArrowRight className="w-4 h-4 text-primary-400" />
                    <span>Detect price anomalies</span>
                  </li>
                </ul>
              </div>
            </div>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleProcess}
              disabled={processing}
              className="w-full px-6 py-4 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-700 text-white font-semibold text-lg
                       disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-xl transition-all flex items-center justify-center space-x-3"
            >
              {processing ? (
                <>
                  <Loader className="w-6 h-6 animate-spin" />
                  <span>Processing... (This may take a few minutes)</span>
                </>
              ) : (
                <>
                  <Zap className="w-6 h-6" />
                  <span>Start Processing</span>
                </>
              )}
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Process Result */}
      <AnimatePresence>
        {processResult && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="glass rounded-2xl p-6 border-l-4 border-green-500"
          >
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 rounded-xl bg-green-500/20 flex items-center justify-center flex-shrink-0">
                <CheckCircle className="w-6 h-6 text-green-400" />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-white mb-4">Processing Complete! 🎉</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                  <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                    <p className="text-sm text-slate-400">Standardized Items</p>
                    <p className="text-2xl font-bold text-blue-400">{processResult.standardized_items}</p>
                  </div>
                  <div className="p-4 bg-purple-500/10 border border-purple-500/30 rounded-lg">
                    <p className="text-sm text-slate-400">Analytics Records</p>
                    <p className="text-2xl font-bold text-purple-400">{processResult.analytics_records}</p>
                  </div>
                  <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
                    <p className="text-sm text-slate-400">Anomalies Found</p>
                    <p className="text-2xl font-bold text-red-400">{processResult.anomalies_found}</p>
                  </div>
                </div>
                <p className="text-green-400 font-medium">
                  ✓ Data has been processed and is now available in the dashboard
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Error Message */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="glass rounded-2xl p-6 border-l-4 border-red-500"
          >
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 rounded-xl bg-red-500/20 flex items-center justify-center flex-shrink-0">
                <AlertCircle className="w-6 h-6 text-red-400" />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-white mb-2">Error</h3>
                <p className="text-red-400">{error}</p>
              </div>
              <button
                onClick={() => setError(null)}
                className="text-slate-400 hover:text-white transition-colors"
              >
                ✕
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Required Format Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass rounded-2xl p-6"
      >
        <h3 className="text-lg font-bold mb-4">📋 Required CSV Format</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-800/50">
              <tr>
                {['po_id', 'item_description', 'unit_price', 'quantity', 'unit', 'po_date', 'region', 'department', 'supplier'].map(col => (
                  <th key={col} className="px-4 py-2 text-left text-slate-300 font-semibold">{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr className="border-t border-slate-700">
                <td className="px-4 py-2 text-slate-400">PO001</td>
                <td className="px-4 py-2 text-slate-400">CS Pipe 100mm</td>
                <td className="px-4 py-2 text-slate-400">1200.00</td>
                <td className="px-4 py-2 text-slate-400">10</td>
                <td className="px-4 py-2 text-slate-400">pcs</td>
                <td className="px-4 py-2 text-slate-400">2024-01-01</td>
                <td className="px-4 py-2 text-slate-400">North</td>
                <td className="px-4 py-2 text-slate-400">Maintenance</td>
                <td className="px-4 py-2 text-slate-400">ABC Metals</td>
              </tr>
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  )
}

export default Upload
