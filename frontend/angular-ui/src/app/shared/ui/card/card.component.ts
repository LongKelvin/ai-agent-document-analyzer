/**
 * Card Component
 *
 * Container component matching the .panel style from backend templates.
 * Provides consistent white background, padding, rounded corners, and border.
 */

import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div [class]="cardClasses">
      <div *ngIf="title" class="mb-6">
        <h2 class="text-xl font-semibold text-gray-900">{{ title }}</h2>
        <p *ngIf="subtitle" class="text-sm text-gray-600 mt-1">{{ subtitle }}</p>
      </div>
      <ng-content></ng-content>
    </div>
  `,
  styles: [`
    :host {
      display: block;
    }
  `]
})
export class CardComponent {
  @Input() title?: string;
  @Input() subtitle?: string;
  @Input() padding: 'none' | 'small' | 'medium' | 'large' = 'medium';
  @Input() noBorder = false;

  get cardClasses(): string {
    const baseClasses = 'bg-white rounded-xl';

    const borderClass = this.noBorder ? '' : 'border border-gray-200';

    const paddingClasses = {
      none: '',
      small: 'p-4',
      medium: 'p-8',
      large: 'p-12'
    };

    return `${baseClasses} ${borderClass} ${paddingClasses[this.padding]}`.trim();
  }
}
