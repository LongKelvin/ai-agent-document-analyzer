/**
 * TypeScript interfaces for Q&A functionality
 * Mirrors Pydantic schemas: QuestionRequest, QuestionResponse
 */

/**
 * Request payload for asking a question
 * Mirrors: QuestionRequest (Pydantic)
 */
export interface QuestionRequest {
  question: string;
  document_id?: string;
}

/**
 * Source reference in Q&A response
 */
export interface QuestionSource {
  source_number: number;
  text: string;
  document: string;
  document_id: string;
}

/**
 * Response from Q&A endpoint
 * Mirrors: QuestionResponse (Pydantic)
 */
export interface QuestionResponse {
  success: boolean;
  answer?: string;
  sources: QuestionSource[];
  error?: string;
}
