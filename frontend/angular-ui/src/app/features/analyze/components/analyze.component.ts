/**
 * Analyze Feature Component
 *
 * Main page for document analysis.
 * Mirrors the behavior of index.html from backend templates.
 */

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DocumentAnalyzerApiService } from '../../../core/api';
import { AnalyzeRequest, AnalyzeResponse, AnalysisResult } from '../../../core/models';
import { ButtonComponent, SpinnerComponent, AlertComponent, CardComponent } from '../../../shared/ui';

type ViewState = 'idle' | 'loading' | 'success' | 'error';

@Component({
  selector: 'app-analyze',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ButtonComponent,
    SpinnerComponent,
    AlertComponent,
    CardComponent
  ],
  templateUrl: './analyze.component.html',
  styleUrls: ['./analyze.component.css']
})
export class AnalyzeComponent {
  documentText = '';
  viewState: ViewState = 'idle';
  analysisResult: AnalysisResult | null = null;
  errorMessage = '';

  constructor(private apiService: DocumentAnalyzerApiService) {}

  get isLoading(): boolean {
    return this.viewState === 'loading';
  }

  get hasResult(): boolean {
    return this.viewState === 'success' && this.analysisResult !== null;
  }

  get hasError(): boolean {
    return this.viewState === 'error';
  }

  get confidencePercent(): number {
    return this.analysisResult ? Math.round(this.analysisResult.confidence * 100) : 0;
  }

  get statusBadgeClass(): string {
    if (!this.analysisResult) return '';

    const statusClasses = {
      complete: 'bg-green-50 text-green-800 border-green-200',
      partial: 'bg-yellow-50 text-yellow-800 border-yellow-200',
      unknown: 'bg-blue-50 text-blue-800 border-blue-200'
    };

    return statusClasses[this.analysisResult.completeness_status] || '';
  }

  onSubmit(): void {
    if (!this.documentText.trim()) {
      this.errorMessage = 'Please enter some text to analyze';
      this.viewState = 'error';
      return;
    }

    this.viewState = 'loading';
    this.analysisResult = null;
    this.errorMessage = '';

    const request: AnalyzeRequest = {
      document_text: this.documentText
    };

    this.apiService.analyze(request).subscribe({
      next: (response: AnalyzeResponse) => {
        if (response.success && response.result) {
          this.analysisResult = response.result;
          this.viewState = 'success';
        } else {
          this.errorMessage = response.error || 'Unknown error occurred';
          this.viewState = 'error';
        }
      },
      error: (error) => {
        this.errorMessage = `Network error: ${error.message}`;
        this.viewState = 'error';
      }
    });
  }
}
