/**
 * Spinner Component
 *
 * Loading indicator with customizable size and color.
 * Used for async operations feedback.
 */

import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-spinner',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div [class]="containerClasses">
      <div [class]="spinnerClasses"></div>
      <p *ngIf="message" class="mt-4 text-gray-600">{{ message }}</p>
    </div>
  `,
  styles: [`
    .spinner {
      border: 3px solid #f3f4f6;
      border-top-color: #1a1a1a;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }
  `]
})
export class SpinnerComponent {
  @Input() size: 'small' | 'medium' | 'large' = 'medium';
  @Input() message?: string;
  @Input() centered = true;

  get containerClasses(): string {
    const base = 'flex flex-col items-center';
    return this.centered ? `${base} justify-center min-h-[200px]` : base;
  }

  get spinnerClasses(): string {
    const sizeMap = {
      small: 'w-6 h-6',
      medium: 'w-12 h-12',
      large: 'w-16 h-16'
    };

    return `spinner ${sizeMap[this.size]}`;
  }
}
