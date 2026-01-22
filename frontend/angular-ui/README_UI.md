# Angular UI - AI Agent Document Analyzer

Frontend application for the AI Agent Document Analyzer built with Angular 18+ and Tailwind CSS.

## Setup Complete ✅

- Angular 18 standalone project
- Tailwind CSS v3 configured
- Proxy configuration for backend API
- Directory structure created
- Environment files configured

## Project Structure

```
src/app/
├── core/
│   ├── api/              # HTTP clients for backend
│   ├── models/           # TypeScript interfaces (mirror Pydantic schemas)
│   └── config/           # API configuration
│
├── features/
│   ├── analyze/          # Document analysis feature
│   ├── documents/        # Upload & Q&A feature
│   └── health/           # Health check feature
│
└── shared/
    └── ui/               # Reusable UI components
```

## Development

```bash
# Install dependencies (already done)
npm install

# Start development server with proxy
npm start

# Build for production
npm run build

# Run tests
npm test
```

## Backend Integration

- **API Proxy**: Configured to proxy `/api` requests to `http://localhost:8000`
- **Environment**: API URL set to `/api` in both development and production
- **No CORS issues**: Proxy handles all backend communication

## Technology Stack

- **Angular 18+** - Standalone components
- **Tailwind CSS v3** - Utility-first styling
- **TypeScript 5+** - Type safety
- **HttpClient** - API communication
- **SSR Enabled** - Server-side rendering support

## Design System

### Colors (from existing templates)
- Primary: `#1a1a1a`
- Secondary: `#2d2d2d`
- Background: `#fafafa`
- Borders: `#e5e5e5`
- Gray shades: 50, 100, 200, 300, 400, 500

### Spacing & Typography
Matches existing HTML templates exactly - no design improvements.

## Next Steps

1. Create TypeScript interfaces (mirror Pydantic schemas)
2. Build API client service
3. Create shared UI components
4. Build feature components (Analyze, Documents, Health)

## Backend Requirements

The FastAPI backend must be running on `http://localhost:8000` for the Angular app to function.

Start backend:
```bash
cd ../../
.\run.ps1
```

Then start Angular:
```bash
cd frontend/angular-ui
npm start
```

Access Angular UI at: `http://localhost:4200`
