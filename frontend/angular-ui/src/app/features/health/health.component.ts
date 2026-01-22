/**
 * Health Check Component
 *
 * Simple page that displays backend health status.
 * Development tool only.
 */

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DocumentAnalyzerApiService } from '../../core/api';
import { HealthCheckResponse } from '../../core/models';
import { SpinnerComponent, AlertComponent, CardComponent } from '../../shared/ui';

type HealthState = 'loading' | 'healthy' | 'error';

@Component({
  selector: 'app-health',
  standalone: true,
  imports: [
    CommonModule,
    SpinnerComponent,
    AlertComponent,
    CardComponent
  ],
  templateUrl: './health.component.html',
  styleUrls: ['./health.component.css']
})
export class HealthComponent implements OnInit {
  healthState: HealthState = 'loading';
  healthData: HealthCheckResponse | null = null;
  errorMessage = '';

  constructor(private apiService: DocumentAnalyzerApiService) {}

  ngOnInit(): void {
    this.checkHealth();
  }

  checkHealth(): void {
    this.healthState = 'loading';
    this.errorMessage = '';

    this.apiService.healthCheck().subscribe({
      next: (response: HealthCheckResponse) => {
        this.healthData = response;
        this.healthState = 'healthy';
      },
      error: (error: any) => {
        this.errorMessage = `Failed to connect: ${error.message}`;
        this.healthState = 'error';
      }
    });
  }

  get isLoading(): boolean {
    return this.healthState === 'loading';
  }

  get isHealthy(): boolean {
    return this.healthState === 'healthy';
  }

  get hasError(): boolean {
    return this.healthState === 'error';
  }

  get statusBadgeClass(): string {
    if (!this.healthData) return '';

    return this.healthData.status === 'healthy'
      ? 'bg-green-50 text-green-800 border-green-200'
      : 'bg-red-50 text-red-800 border-red-200';
  }
}
