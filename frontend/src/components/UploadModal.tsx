import React, { useCallback, useState } from 'react'
import { Upload, X, FileText, AlertCircle, CheckCircle, Cloud, FolderOpen, Loader } from 'lucide-react'
import { cn } from '@/utils/cn'
import type { UploadFile } from '@/types/context'

interface UploadModalProps {
  isOpen: boolean
  onClose: () => void
  onUpload: (files: UploadFile[]) => void
}

export function UploadModal({ isOpen, onClose, onUpload }: UploadModalProps) {
  const [dragActive, setDragActive] = useState(false)
  const [uploadFiles, setUploadFiles] = useState<UploadFile[]>([])

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const files = Array.from(e.dataTransfer.files)
      const validFiles = files.filter(file => file.name.endsWith('.ct'))
      
      const newUploadFiles: UploadFile[] = validFiles.map(file => ({
        file,
        name: file.name,
        size: `${(file.size / 1024).toFixed(1)} KB`,
        status: 'uploading'
      }))
      
      setUploadFiles(prev => [...prev, ...newUploadFiles])
    }
  }, [])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files
    if (selectedFiles && selectedFiles.length > 0) {
      const files = Array.from(selectedFiles)
      const validFiles = files.filter(file => file.name.endsWith('.ct'))
      
      const newUploadFiles: UploadFile[] = validFiles.map(file => ({
        file,
        name: file.name,
        size: `${(file.size / 1024).toFixed(1)} KB`,
        status: 'uploading'
      }))
      
      setUploadFiles(prev => [...prev, ...newUploadFiles])
    }
  }

  const handleUpload = async () => {
    if (uploadFiles.length === 0) return

    // 模拟上传过程
    const updatedFiles = uploadFiles.map(file => ({
      ...file,
      status: 'success' as const
    }))
    
    setUploadFiles(updatedFiles)
    
    // 延迟关闭模态框
    setTimeout(() => {
      onUpload(updatedFiles)
      onClose()
      setUploadFiles([])
    }, 1000)
  }

  const removeFile = (index: number) => {
    setUploadFiles(prev => prev.filter((_, i) => i !== index))
  }

  if (!isOpen) return null

  const validFiles = uploadFiles.filter(f => f.status !== 'error').length
  const totalFiles = uploadFiles.length
  const progressPercentage = totalFiles > 0 ? (validFiles / totalFiles) * 100 : 0

  return (
    <div 
      className="fixed inset-0 bg-opacity-50 flex items-center justify-center z-50"
      style={{ backgroundColor: 'rgba(7, 11, 17, 0.5)' }}
    >
      <div 
        className="overflow-hidden w-[600px] rounded-lg shadow-xl"
        style={{ backgroundColor: 'rgba(255, 255, 255, 1)' }}
      >
        <div className="header flex justify-between items-center px-6">
          <h2 
            className="text-xl font-medium"
            style={{ color: 'rgba(7, 11, 17, 1)' }}
          >
            上传上下文文件
          </h2>
          <button
            onClick={onClose}
            className="flex justify-center items-center w-10 h-10 hover:bg-gray-100 rounded transition-colors"
            style={{ color: 'rgba(136, 138, 139, 1)' }}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="pt-6 pr-6 pb-6 pl-6">
          <div
            className={cn(
              "upload-area flex flex-col justify-center items-center mb-6 pt-6 pr-6 pb-6 pl-6",
              dragActive && "border-gray-900"
            )}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div 
              className="flex justify-center items-center w-16 h-16 mb-4 rounded-md"
              style={{ backgroundColor: 'rgba(33, 37, 40, 1)' }}
            >
              <Cloud className="w-6 h-6 text-white" />
            </div>
            <p 
              className="mb-2 text-sm font-medium"
              style={{ color: 'rgba(7, 11, 17, 1)' }}
            >
              拖放 .ct 文件到此处
            </p>
            <p 
              className="mb-4 text-xs"
              style={{ color: 'rgba(136, 138, 139, 1)' }}
            >
              或者
            </p>
            <label className="btn btn-primary btn-sm cursor-pointer">
              <FolderOpen className="w-4 h-4 mr-2" />
              浏览文件
              <input
                type="file"
                accept=".ct"
                multiple
                onChange={handleFileSelect}
                className="hidden"
              />
            </label>
          </div>

          {uploadFiles.length > 0 && (
            <div className="mb-6">
              <h3 
                className="mb-3 text-sm font-medium"
                style={{ color: 'rgba(7, 11, 17, 1)' }}
              >
                文件列表
              </h3>
              <div className="space-y-3">
                {uploadFiles.map((file, index) => (
                  <div 
                    key={index} 
                    className="flex items-center pt-4 pr-4 pb-4 pl-4 rounded-md"
                    style={{ backgroundColor: 'rgba(244, 246, 248, 1)' }}
                  >
                    <div 
                      className="flex justify-center items-center w-8 h-8 mr-3 rounded-md"
                      style={{ backgroundColor: 'rgba(33, 37, 40, 1)' }}
                    >
                      <FileText className="w-4 h-4 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex justify-between items-center">
                        <h4 
                          className="text-sm font-medium truncate"
                          style={{ color: 'rgba(7, 11, 17, 1)' }}
                        >
                          {file.name}
                        </h4>
                        <span 
                          className="flex items-center text-xs ml-2"
                          style={{ 
                            color: file.status === 'success' 
                              ? 'rgba(61, 191, 154, 1)' 
                              : file.status === 'error'
                              ? 'rgba(223, 108, 108, 1)'
                              : 'rgba(136, 138, 139, 1)'
                          }}
                        >
                          {file.status === 'success' ? (
                            <>
                              <CheckCircle className="w-3 h-3 mr-1" />
                              验证通过
                            </>
                          ) : file.status === 'error' ? (
                            <>
                              <AlertCircle className="w-3 h-3 mr-1" />
                              格式错误
                            </>
                          ) : (
                            <>
                              <Loader className="w-3 h-3 mr-1 animate-spin" />
                              正在验证
                            </>
                          )}
                        </span>
                      </div>
                      <div className="flex items-center mt-1">
                        <span 
                          className="text-xs"
                          style={{ color: 'rgba(136, 138, 139, 1)' }}
                        >
                          {file.size}
                        </span>
                      </div>
                    </div>
                    <button
                      onClick={() => removeFile(index)}
                      className="ml-2 hover:bg-gray-200 p-1 rounded"
                      style={{ color: 'rgba(136, 138, 139, 1)' }}
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {uploadFiles.length > 0 && (
            <div className="mb-6">
              <div className="flex justify-between items-center mb-2">
                <span 
                  className="text-xs"
                  style={{ color: 'rgba(7, 11, 17, 1)' }}
                >
                  上传进度
                </span>
                <span 
                  className="text-xs"
                  style={{ color: 'rgba(136, 138, 139, 1)' }}
                >
                  {validFiles}/{totalFiles} 文件
                </span>
              </div>
              <div className="progress-bar">
                <div 
                  className="progress-fill transition-all duration-300"
                  style={{ width: `${progressPercentage}%` }}
                />
              </div>
            </div>
          )}

          <div className="flex justify-end gap-3">
            <button
              onClick={onClose}
              className="btn btn-secondary btn-sm"
            >
              取消
            </button>
            <button
              onClick={handleUpload}
              className="btn btn-primary btn-sm"
              disabled={uploadFiles.length === 0}
            >
              上传
            </button>
          </div>
        </div>
      </div>
    </div>
  )
} 