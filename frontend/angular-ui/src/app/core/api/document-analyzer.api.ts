/**
 * Document Analyzer API Service
 *
 * Typed HTTP client for all backend API endpoints.
 * This service is the ONLY place where HTTP calls should be made.
 *
 * All methods return Observables that match backend Pydantic response schemas exactly.
 * No transformation or interpretation of responses - display what the backend returns.
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BASE_URL } from '../config/api.config';
import {
  AnalyzeRequest,
  AnalyzeResponse,
  DocumentUploadResponse,
  DocumentListResponse,
  DocumentDeleteResponse,
  QuestionRequest,
  QuestionResponse,
  HealthCheckResponse
} from '../models';

@Injectable({
  providedIn: 'root'
})
export class DocumentAnalyzerApiService {
  private readonly baseUrl = API_BASE_URL;

  constructor(private http: HttpClient) {}

  /**
   * Analyze a document for completeness and clarity
   *
   * POST /analyze
   *
   * @param request - Document text to analyze
   * @returns Observable<AnalyzeResponse> - Validated analysis result from LLM
   */
  analyze(request: AnalyzeRequest): Observable<AnalyzeResponse> {
    return this.http.post<AnalyzeResponse>(`${this.baseUrl}/analyze`, request);
  }

  /**
   * Upload a document to the vector database
   *
   * POST /upload
   *
   * Supports: .txt, .md, .pdf files
   *
   * @param file - File to upload
   * @returns Observable<DocumentUploadResponse> - Upload result with document ID
   */
  uploadDocument(file: File): Observable<DocumentUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    console.log('[API Service] Uploading file:', file.name);
    console.log('[API Service] FormData created, making POST request to:', `${this.baseUrl}/upload`);

    const upload$ = this.http.post<DocumentUploadResponse>(`${this.baseUrl}/upload`, formData);
    console.log('[API Service] Observable created:', upload$);

    return upload$;
  }

  /**
   * Ask a question about uploaded documents using RAG
   *
   * POST /ask
   *
   * @param request - Question and optional document ID filter
   * @returns Observable<QuestionResponse> - Answer with source citations
   */
  askQuestion(request: QuestionRequest): Observable<QuestionResponse> {
    console.log('[API Service] Asking question:', request.question);
    return this.http.post<QuestionResponse>(`${this.baseUrl}/ask`, request);
  }

  /**
   * List all uploaded documents
   *
   * GET /documents
   *
   * @returns Observable<DocumentListResponse> - List of documents with metadata
   */
  listDocuments(): Observable<DocumentListResponse> {
    console.log('[API Service] Fetching document list from:', `${this.baseUrl}/documents`);
    return this.http.get<DocumentListResponse>(`${this.baseUrl}/documents`);
  }

  /**
   * Delete a document from the vector database
   *
   * DELETE /documents/{document_id}
   *
   * @param documentId - ID of document to delete
   * @returns Observable<DocumentDeleteResponse> - Deletion result
   */
  deleteDocument(documentId: string): Observable<DocumentDeleteResponse> {
    console.log('[API Service] Deleting document:', documentId);
    return this.http.delete<DocumentDeleteResponse>(`${this.baseUrl}/documents/${documentId}`);
  }

  /**
   * Check backend health status
   *
   * GET /health
   *
   * Used for development visibility and monitoring
   *
   * @returns Observable<HealthCheckResponse> - Backend status
   */
  healthCheck(): Observable<HealthCheckResponse> {
    return this.http.get<HealthCheckResponse>(`${this.baseUrl}/health`);
  }
}
