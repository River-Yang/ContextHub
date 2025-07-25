// API 工具函数
const API_BASE_URL = 'http://localhost:5001/api'

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface UploadResult {
  filename: string
  status: 'success' | 'error'
  id?: string
  saved_as?: string
  error?: string
  warnings?: string[]
  details?: string[]
}

export interface UploadResponse {
  success: boolean
  message: string
  results: UploadResult[]
  uploaded_files: any[]
}

export interface CreateResult {
  filename: string
  status: 'success' | 'error'
  id?: string
  ct_filename?: string
  error?: string
  message?: string
}

export interface CreateResponse {
  success: boolean
  message: string
  results: CreateResult[]
  created_contexts: any[]
}

// 健康检查
export async function healthCheck(): Promise<ApiResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`)
    return await response.json()
  } catch (error) {
    return {
      success: false,
      error: `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`
    }
  }
}

// 获取所有上下文文件
export async function getContexts(): Promise<ApiResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/contexts`)
    return await response.json()
  } catch (error) {
    return {
      success: false,
      error: `Failed to fetch contexts: ${error instanceof Error ? error.message : 'Unknown error'}`
    }
  }
}

// 获取特定上下文文件详情
export async function getContext(contextId: string): Promise<ApiResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/contexts/${contextId}`)
    return await response.json()
  } catch (error) {
    return {
      success: false,
      error: `Failed to fetch context: ${error instanceof Error ? error.message : 'Unknown error'}`
    }
  }
}

// 上传文件
export async function uploadFiles(files: File[]): Promise<UploadResponse> {
  try {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData
    })

    return await response.json()
  } catch (error) {
    return {
      success: false,
      message: `Upload failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
      results: [],
      uploaded_files: []
    }
  }
}

// 创建上下文文件（从各种文件格式转换）
export async function createContextFromFiles(files: File[]): Promise<CreateResponse> {
  try {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })

    const response = await fetch(`${API_BASE_URL}/create`, {
      method: 'POST',
      body: formData
    })

    return await response.json()
  } catch (error) {
    return {
      success: false,
      message: `Create failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
      results: [],
      created_contexts: []
    }
  }
}

// 下载文件
export async function downloadContext(contextId: string): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/download/${contextId}`)
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Download failed')
    }

    // 获取文件名
    const contentDisposition = response.headers.get('Content-Disposition')
    let filename = 'context.ct'
    
    if (contentDisposition) {
      const match = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)
      if (match && match[1]) {
        filename = match[1].replace(/['"]/g, '')
      }
    }

    // 创建下载链接
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    throw new Error(`Download failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}

// 删除上下文文件
export async function deleteContext(contextId: string): Promise<ApiResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/contexts/${contextId}`, {
      method: 'DELETE'
    })
    return await response.json()
  } catch (error) {
    return {
      success: false,
      error: `Failed to delete context: ${error instanceof Error ? error.message : 'Unknown error'}`
    }
  }
}

// 验证上下文文件
export async function validateContext(file: File): Promise<ApiResponse> {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${API_BASE_URL}/validate`, {
      method: 'POST',
      body: formData
    })

    return await response.json()
  } catch (error) {
    return {
      success: false,
      error: `Validation failed: ${error instanceof Error ? error.message : 'Unknown error'}`
    }
  }
} 