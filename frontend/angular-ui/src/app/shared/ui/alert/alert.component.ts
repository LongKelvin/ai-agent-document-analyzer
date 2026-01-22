/**
 * Alert Component
 *
 * Displays success, error, warning, or info messages.
 * Supports dismissible alerts with close button.
 */

import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-alert',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="visible" [class]="alertClasses" role="alert">
      <div class="flex items-start">
        <span class="text-xl mr-3">{{ icon }}</span>
        <div class="flex-1">
          <p *ngIf="title" class="font-semibold mb-1">{{ title }}</p>
          <p class="text-sm">{{ message }}</p>
        </div>
        <button
          *ngIf="dismissible"
          type="button"
          class="ml-4 text-current opacity-70 hover:opacity-100 transition-opacity"
          (click)="close()"
          aria-label="Close"
        >
          ✕
        </button>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
    }
  `]
})
export class AlertComponent {
  @Input() type: 'success' | 'error' | 'warning' | 'info' = 'info';
  @Input() title?: string;
  @Input() message = '';
  @Input() dismissible = true;
  @Input() visible = true;

  @Output() dismissed = new EventEmitter<void>();

  get alertClasses(): string {
    const baseClasses = 'p-4 rounded-lg border mb-4';

    const typeClasses = {
      success: 'bg-green-50 border-green-200 text-green-800',
      error: 'bg-red-50 border-red-200 text-red-800',
      warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
      info: 'bg-blue-50 border-blue-200 text-blue-800'
    };

    return `${baseClasses} ${typeClasses[this.type]}`;
  }

  get icon(): string {
    const icons = {
      success: '✓',
      error: '✕',
      warning: '⚠',
      info: 'ℹ'
    };

    return icons[this.type];
  }

  close(): void {
    this.visible = false;
    this.dismissed.emit();
  }
}
