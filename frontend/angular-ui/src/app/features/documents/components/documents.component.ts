/**
 * Documents Feature Component
 *
 * Provides three tabs: Upload, Q&A, and Document Management.
 * Mirrors the behavior of advanced.html from backend templates.
 */

import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DocumentAnalyzerApiService } from '../../../core/api';
import {
  DocumentUploadResponse,
  DocumentInfo,
  DocumentListResponse,
  QuestionRequest,
  QuestionResponse,
  QuestionSource
} from '../../../core/models';
import { ButtonComponent, SpinnerComponent, AlertComponent, CardComponent } from '../../../shared/ui';

type TabType = 'upload' | 'qa' | 'documents';
type UploadState = 'idle' | 'uploading' | 'success' | 'error';
type QaState = 'idle' | 'loading' | 'success' | 'error';

@Component({
  selector: 'app-documents',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ButtonComponent,
    SpinnerComponent,
    AlertComponent,
    CardComponent
  ],
  templateUrl: './documents.component.html',
  styleUrls: ['./documents.component.css']
})
export class DocumentsComponent implements OnInit {
  activeTab: TabType = 'upload';

  // Upload Tab State
  uploadState: UploadState = 'idle';
  selectedFile: File | null = null;
  uploadMessage = '';
  uploadError = '';
  dragOver = false;

  // Q&A Tab State
  qaState: QaState = 'idle';
  question = '';
  answer = '';
  sources: QuestionSource[] = [];
  qaError = '';
  selectedDocumentId = '';

  // Documents Tab State
  documents: DocumentInfo[] = [];
  loadingDocuments = false;
  documentsError = '';

  constructor(
    private apiService: DocumentAnalyzerApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadDocuments();
  }

  // Tab Management
  switchTab(tab: TabType): void {
    this.activeTab = tab;
    if (tab === 'documents') {
      this.loadDocuments();
    }
  }

  // Upload Tab Methods
  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      this.uploadState = 'idle';
      this.uploadMessage = '';
      this.uploadError = '';
    }
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.dragOver = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.dragOver = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.dragOver = false;

    if (event.dataTransfer?.files && event.dataTransfer.files.length > 0) {
      this.selectedFile = event.dataTransfer.files[0];
      this.uploadState = 'idle';
      this.uploadMessage = '';
      this.uploadError = '';
    }
  }

  triggerFileInput(): void {
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    fileInput?.click();
  }

  uploadFile(): void {
    if (!this.selectedFile) {
      this.uploadError = 'Please select a file';
      this.uploadState = 'error';
      return;
    }

    this.uploadState = 'uploading';
    this.uploadMessage = '';
    this.uploadError = '';

    console.log('[DocumentsComponent] Starting upload:', this.selectedFile.name);

    const upload$ = this.apiService.uploadDocument(this.selectedFile);
    console.log('[DocumentsComponent] Observable created:', upload$);

    upload$.subscribe({
      next: (response: DocumentUploadResponse) => {
        console.log('[DocumentsComponent] NEXT callback triggered');
        console.log('[DocumentsComponent] Received response:', response);
        console.log('[DocumentsComponent] Response type:', typeof response);
        console.log('[DocumentsComponent] Response keys:', Object.keys(response));

        if (response.success) {
          this.uploadMessage = response.message;
          this.uploadState = 'success';
          this.selectedFile = null;
          // Reset file input
          const fileInput = document.getElementById('fileInput') as HTMLInputElement;
          if (fileInput) fileInput.value = '';
          console.log('[DocumentsComponent] Upload successful');
          this.cdr.detectChanges(); // Force change detection
        } else {
          this.uploadError = response.error || 'Upload failed';
          this.uploadState = 'error';
          console.error('[DocumentsComponent] Upload failed:', response.error);
          this.cdr.detectChanges(); // Force change detection
        }
      },
      error: (error) => {
        console.error('[DocumentsComponent] ERROR callback triggered');
        console.error('[DocumentsComponent] Upload error:', error);
        this.uploadError = `Network error: ${error.message}`;
        this.uploadState = 'error';
      },
      complete: () => {
        console.log('[DocumentsComponent] COMPLETE callback triggered');
        console.log('[DocumentsComponent] Current uploadState:', this.uploadState);
      }
    });
  }

  get isUploading(): boolean {
    return this.uploadState === 'uploading';
  }

  // Q&A Tab Methods
  askQuestion(): void {
    if (!this.question.trim()) {
      this.qaError = 'Please enter a question';
      this.qaState = 'error';
      return;
    }

    this.qaState = 'loading';
    this.answer = '';
    this.sources = [];
    this.qaError = '';

    const request: QuestionRequest = {
      question: this.question,
      document_id: this.selectedDocumentId || undefined
    };

    console.log('[DocumentsComponent] Asking question:', request);

    this.apiService.askQuestion(request).subscribe({
      next: (response: QuestionResponse) => {
        console.log('[DocumentsComponent] Q&A response:', response);
        if (response.success && response.answer) {
          this.answer = response.answer;
          this.sources = response.sources || [];
          this.qaState = 'success';
          console.log('[DocumentsComponent] Q&A successful, sources:', this.sources.length);
          this.cdr.detectChanges();
        } else {
          this.qaError = response.error || 'Failed to get answer';
          this.qaState = 'error';
          console.error('[DocumentsComponent] Q&A failed:', response.error);
          this.cdr.detectChanges();
        }
      },
      error: (error) => {
        console.error('[DocumentsComponent] Q&A error:', error);
        this.qaError = `Network error: ${error.message}`;
        this.qaState = 'error';
        this.cdr.detectChanges();
      },
      complete: () => {
        console.log('[DocumentsComponent] Q&A observable completed, state:', this.qaState);
      }
    });
  }

  get isQaLoading(): boolean {
    return this.qaState === 'loading';
  }

  get hasAnswer(): boolean {
    return this.qaState === 'success' && !!this.answer;
  }

  // Documents Tab Methods
  loadDocuments(): void {
    this.loadingDocuments = true;
    this.documentsError = '';

    console.log('[DocumentsComponent] Loading documents...');

    this.apiService.listDocuments().subscribe({
      next: (response: DocumentListResponse) => {
        console.log('[DocumentsComponent] Documents response:', response);
        if (response.success) {
          this.documents = response.documents;
          this.loadingDocuments = false;
          console.log('[DocumentsComponent] Loaded', this.documents.length, 'documents');
          this.cdr.detectChanges();
        } else {
          this.documentsError = response.error || 'Failed to load documents';
          this.loadingDocuments = false;
          console.error('[DocumentsComponent] Load failed:', response.error);
          this.cdr.detectChanges();
        }
      },
      error: (error) => {
        console.error('[DocumentsComponent] Load error:', error);
        this.documentsError = `Network error: ${error.message}`;
        this.loadingDocuments = false;
        this.cdr.detectChanges();
      },
      complete: () => {
        console.log('[DocumentsComponent] Load documents observable completed');
      }
    });
  }

  deleteDocument(documentId: string): void {
    if (!confirm('Are you sure you want to delete this document?')) {
      return;
    }

    console.log('[DocumentsComponent] Deleting document:', documentId);

    this.apiService.deleteDocument(documentId).subscribe({
      next: (response) => {
        console.log('[DocumentsComponent] Delete response:', response);
        if (response.success) {
          console.log('[DocumentsComponent] Delete successful, reloading list');
          this.loadDocuments(); // Reload the list
        } else {
          this.documentsError = response.error || 'Failed to delete document';
          console.error('[DocumentsComponent] Delete failed:', response.error);
          this.cdr.detectChanges();
        }
      },
      error: (error) => {
        console.error('[DocumentsComponent] Delete error:', error);
        this.documentsError = `Network error: ${error.message}`;
        this.cdr.detectChanges();
      },
      complete: () => {
        console.log('[DocumentsComponent] Delete observable completed');
      }
    });
  }

  formatFileSize(bytes: number): string {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  }
}
