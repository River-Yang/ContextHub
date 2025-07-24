// 简化的上下文文件数据结构
export interface ContextFile {
  id: string
  name: string
  description: string
  updated_at: string
  size: string
  system_prompt?: string
  conversation?: Message[]
  assets?: Asset[]
}

export interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
}

export interface Asset {
  id: string
  name: string
  type: string
  size: string
  url?: string
}

// 上传文件的状态
export interface UploadFile {
  file: File
  name: string
  size: string
  status: 'uploading' | 'success' | 'error'
  error?: string
} 