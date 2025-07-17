import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import { Upload as UploadIcon, CheckCircle, FileText } from 'lucide-react'

const Upload = () => {
  const [files, setFiles] = useState([])
  const [isUploading, setIsUploading] = useState(false)
  const [progress, setProgress] = useState(0)

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: 'application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    onDrop: (acceptedFiles) => {
      setFiles(
        acceptedFiles.map((file) =>
          Object.assign(file, {
            preview: URL.createObjectURL(file),
          })
        )
      )
    },
  })

  const handleUpload = () => {
    setIsUploading(true)
    setProgress(0)
    toast.success('Files uploaded successfully')

    // Mock progress update
    const interval = setInterval(() => {
      setProgress((oldProgress) => {
        if (oldProgress === 100) {
          clearInterval(interval)
          setIsUploading(false)
          return 100
        }
        return Math.min(oldProgress + 10, 100)
      })
    }, 200)
  }

  return (
    <div className="min-h-screen bg-zinc-900 flex items-center justify-center p-8">
      <div className="w-full max-w-lg">
        {/* Upload Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h2 className="text-3xl font-bold glow-text">Upload Documents</h2>
          <p className="text-zinc-1000 mt-2">
            Drop your files here or click to upload
          </p>
        </motion.div>

        {/* Dropzone */}
        <motion.div
          {...getRootProps()}
          initial={{ scale: 0.95 }}
          animate={{ scale: 1 }}
          whileHover={{ scale: 1.02 }}
          transition={{ duration: 0.4 }}
          className={`border-dashed border-2 p-6 rounded-lg cursor-pointer mb-6 transition-all duration-300 
            ${isDragActive ? 'border-purple-500 bg-purple-50/10' : 'border-zinc-700 bg-zinc-800/40 hover:bg-zinc-800/30'}`}
        >
          <input {...getInputProps()} />
          {isDragActive ? (
            <p className="flex items-center justify-center space-x-2">
              <UploadIcon className="w-5 h-5 text-purple-400 animate-bounce" />
              <span className="text-zinc-1000">Drop the files here ...</span>
            </p>
          ) : (
            <p className="flex items-center justify-center space-x-2">
              <UploadIcon className="w-5 h-5 text-zinc-600" />
              <span className="text-zinc-1000">Drag and drop some files here, or click to select files</span>
            </p>
          )}
        </motion.div>

        {/* File List */}
        {files.length > 0 && (
          <motion.ul
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="space-y-2 mb-4"
          >
            {files.map((file, index) => (
              <li key={index} className="flex items-center justify-between p-2 bg-zinc-800/50 rounded-lg">
                <div className="flex items-center space-x-2">
                  <FileText className="w-5 h-5 text-purple-400" />
                  <span className="text-zinc-600">{file.name}</span>
                </div>
                {isUploading ? (
                  <span className="text-zinc-1000 text-sm">Uploading...</span>
                ) : (
                  <CheckCircle className="w-5 h-5 text-green-400" />
                )}
              </li>
            ))}
          </motion.ul>
        )}

        {/* Upload Button & Progress */}
        {files.length > 0 && !isUploading && (
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="btn-primary w-full"
            onClick={handleUpload}
          >
            Start Upload
          </motion.button>
        )}

        {isUploading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="w-full bg-zinc-700 rounded-full h-2 mt-4 mb-2"
          >
            <div
              className="bg-gradient-to-r from-purple-500 to-primary-500 h-2 rounded-full"
              style={{ width: `${progress}%` }}
            />
          </motion.div>
        )}
      </div>
    </div>
  )
}

export default Upload


