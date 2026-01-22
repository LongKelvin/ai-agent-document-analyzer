/**
 * TypeScript interfaces for document management
 * Mirrors Pydantic schemas: DocumentUploadResponse, DocumentInfo, DocumentListResponse
 */

/**
 * Response from document upload endpoint
 * Mirrors: DocumentUploadResponse (Pydantic)
 */
export interface DocumentUploadResponse {
  success: boolean;
  document_id?: string;
  filename?: string;
  message: string;
  error?: string;
}

/**
 * Information about a stored document
 * Mirrors: DocumentInfo (Pydantic)
 */
export interface DocumentInfo {
  document_id: string;
  filename: string;
  upload_date: string;
  file_size: number;
}

/**
 * Response from list documents endpoint
 * Mirrors: DocumentListResponse (Pydantic)
 */
export interface DocumentListResponse {
  success: boolean;
  documents: DocumentInfo[];
  total_count: number;
  error?: string;
}

/**
 * Response from delete document endpoint
 */
export interface DocumentDeleteResponse {
  success: boolean;
  message: string;
  error?: string;
}
