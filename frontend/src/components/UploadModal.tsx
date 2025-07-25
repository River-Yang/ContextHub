import React, { useCallback, useState } from 'react'
import { Plus, X, FileText, AlertCircle, CheckCircle, Cloud, FolderOpen, Loader } from 'lucide-react'
import { cn } from '@/utils/cn'
import type { UploadFile } from '@/types/context'
import { createContextFromFiles as apiCreateFiles } from '@/utils/api'

interface CreateModalProps {
  isOpen: boolean
  onClose: () => void
  onCreate: (files: UploadFile[]) => void
}

export function CreateModal({ isOpen, onClose, onCreate }: CreateModalProps) {
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
      
      const newUploadFiles: UploadFile[] = files.map(file => ({
        file,
        name: file.name,
        size: `${(file.size / 1024).toFixed(1)} KB`,
        status: 'ready'
      }))
      
      setUploadFiles(prev => [...prev, ...newUploadFiles])
    }
  }, [])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files
    if (selectedFiles && selectedFiles.length > 0) {
      const files = Array.from(selectedFiles)
      
      const newUploadFiles: UploadFile[] = files.map(file => ({
        file,
        name: file.name,
        size: `${(file.size / 1024).toFixed(1)} KB`,
        status: 'ready'
      }))
      
      setUploadFiles(prev => [...prev, ...newUploadFiles])
    }
  }

  const handleCreate = async () => {
    if (uploadFiles.length === 0) return

    try {
      // 更新所有文件状态为上传中
      setUploadFiles(prev => prev.map(file => ({
        ...file,
        status: 'uploading' as const
      })))

      // 提取实际的File对象
      const filesToUpload = uploadFiles.map(f => f.file)
      
      // 调用API创建上下文文件
      const response = await apiCreateFiles(filesToUpload)
      
      if (response.success) {
        // 根据API响应更新文件状态
                 const updatedFiles = uploadFiles.map(file => {
           const result = response.results.find((r: any) => r.filename === file.name)
          if (result) {
            return {
              ...file,
              status: result.status as 'success' | 'error',
              error: result.error
            }
          }
          return file
        })
        
        setUploadFiles(updatedFiles)
        
        // 延迟关闭模态框，给用户时间看到结果
        setTimeout(() => {
          const successFiles = updatedFiles.filter(f => f.status === 'success')
          if (successFiles.length > 0) {
            onCreate(successFiles)
          }
          onClose()
          setUploadFiles([])
        }, 1500)
      } else {
        // 上传失败，显示错误
        setUploadFiles(prev => prev.map(file => ({
          ...file,
          status: 'error' as const,
          error: response.message || 'Upload failed'
        })))
      }
    } catch (error) {
      // 网络错误或其他异常
      setUploadFiles(prev => prev.map(file => ({
        ...file,
        status: 'error' as const,
        error: error instanceof Error ? error.message : 'Upload failed'
      })))
    }
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
            新建上下文文件
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
              拖放文件到此处，自动转换为 .ct 格式
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
                accept=".py,.js,.ts,.tsx,.jsx,.java,.cpp,.c,.h,.hpp,.cs,.php,.rb,.go,.rs,.swift,.kt,.scala,.sh,.bash,.zsh,.html,.css,.scss,.sass,.md,.xml,.vue,.json,.yaml,.yml,.toml,.ini,.cfg,.sql,.r,.m,.pl,.lua,.dart,.txt,.rst,.jpg,.jpeg,.png,.gif,.bmp,.tiff,.webp"
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
                              转换成功
                            </>
                          ) : file.status === 'error' ? (
                            <>
                              <AlertCircle className="w-3 h-3 mr-1" />
                              {file.error || '转换失败'}
                            </>
                          ) : file.status === 'uploading' ? (
                            <>
                              <Loader className="w-3 h-3 mr-1 animate-spin" />
                              转换中...
                            </>
                          ) : (
                            <>
                              <FileText className="w-3 h-3 mr-1" />
                              准备转换
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
                  转换进度
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
              onClick={handleCreate}
              className="btn btn-primary btn-sm"
              disabled={uploadFiles.length === 0}
            >
              新建
            </button>
          </div>
        </div>
      </div>
    </div>
  )
} 