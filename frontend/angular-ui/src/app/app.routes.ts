import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'analyze',
    pathMatch: 'full'
  },
  {
    path: 'analyze',
    loadComponent: () => import('./features/analyze/components/analyze.component').then(m => m.AnalyzeComponent),
    data: { prerender: false }
  },
  {
    path: 'documents',
    loadComponent: () => import('./features/documents/components/documents.component').then(m => m.DocumentsComponent),
    data: { prerender: false }
  },
  {
    path: 'health',
    loadComponent: () => import('./features/health/health.component').then(m => m.HealthComponent),
    data: { prerender: false }
  },
  {
    path: '**',
    redirectTo: 'analyze'
  }
];
