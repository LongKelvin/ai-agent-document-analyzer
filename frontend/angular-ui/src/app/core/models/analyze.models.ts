/**
 * TypeScript interfaces mirroring Pydantic schemas from app/models/schemas.py
 *
 * These interfaces define the exact data contracts between Angular UI and FastAPI backend.
 * DO NOT modify these without updating the corresponding Pydantic models.
 */

/**
 * Completeness status literal type
 * Mirrors: Literal["complete", "partial", "unknown"]
 */
export type CompletenessStatus = 'complete' | 'partial' | 'unknown';

/**
 * Analysis result from AI agent
 * Mirrors: AnalysisResult (Pydantic)
 */
export interface AnalysisResult {
  summary: string;
  completeness_status: CompletenessStatus;
  missing_points: string[];
  evidence: string[];
  confidence: number;
}

/**
 * Request payload for document analysis
 * Mirrors: AnalyzeRequest (Pydantic)
 */
export interface AnalyzeRequest {
  document_text: string;
}

/**
 * Response from document analysis endpoint
 * Mirrors: AnalyzeResponse (Pydantic)
 */
export interface AnalyzeResponse {
  success: boolean;
  result?: AnalysisResult;
  error?: string;
}
