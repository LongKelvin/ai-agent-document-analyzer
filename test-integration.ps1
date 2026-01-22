# Integration Test Script
# Run this to verify backend and frontend integration

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Backend & Frontend Integration Test" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Backend Schema Validation
Write-Host "[TEST 1] Backend Schema Validation..." -ForegroundColor Yellow
try {
    cd backend
    python -c "from app.models.schemas import AnalyzeResponse, DocumentUploadResponse, DocumentDeleteResponse, QuestionResponse, HealthCheckResponse; print('✅ All schemas valid')"
    Write-Host "✅ PASS: All backend schemas imported successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ FAIL: Backend schema import failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 2: Backend Routes Validation
Write-Host "[TEST 2] Backend Routes Validation..." -ForegroundColor Yellow
try {
    python -c "from app.api.routes import router; routes = [r.path for r in router.routes]; print(f'Routes: {routes}'); assert '/analyze' in routes"
    Write-Host "✅ PASS: Backend routes loaded successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ FAIL: Backend routes validation failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 3: Frontend Build
Write-Host "[TEST 3] Frontend Build Validation..." -ForegroundColor Yellow
try {
    cd ../frontend/angular-ui
    npm run build 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ PASS: Frontend builds successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ FAIL: Frontend build failed" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ FAIL: Frontend build error" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 4: Frontend TypeScript Models
Write-Host "[TEST 4] Frontend TypeScript Models..." -ForegroundColor Yellow
$modelsExist = Test-Path "src/app/core/models/analyze.models.ts"
$modelsExist = $modelsExist -and (Test-Path "src/app/core/models/document.models.ts")
$modelsExist = $modelsExist -and (Test-Path "src/app/core/models/qa.models.ts")
$modelsExist = $modelsExist -and (Test-Path "src/app/core/models/health.models.ts")

if ($modelsExist) {
    Write-Host "✅ PASS: All TypeScript models exist" -ForegroundColor Green
} else {
    Write-Host "❌ FAIL: Missing TypeScript model files" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 5: API Service Validation
Write-Host "[TEST 5] API Service Validation..." -ForegroundColor Yellow
if (Test-Path "src/app/core/api/document-analyzer.api.ts") {
    Write-Host "✅ PASS: DocumentAnalyzerApiService exists" -ForegroundColor Green
} else {
    Write-Host "❌ FAIL: API service not found" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 6: Proxy Configuration
Write-Host "[TEST 6] Proxy Configuration..." -ForegroundColor Yellow
if (Test-Path "proxy.conf.json") {
    $proxyConfig = Get-Content "proxy.conf.json" | ConvertFrom-Json
    if ($proxyConfig."/api".target -eq "http://localhost:8000") {
        Write-Host "✅ PASS: Proxy configured correctly" -ForegroundColor Green
    } else {
        Write-Host "❌ FAIL: Proxy target incorrect" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ FAIL: Proxy configuration missing" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "================================" -ForegroundColor Cyan
Write-Host "✅ ALL INTEGRATION TESTS PASSED" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Terminal 1 (Backend):" -ForegroundColor Cyan
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python -m app.main" -ForegroundColor White
Write-Host ""
Write-Host "Terminal 2 (Frontend):" -ForegroundColor Cyan
Write-Host "  cd frontend/angular-ui" -ForegroundColor White
Write-Host "  npm start" -ForegroundColor White
Write-Host ""
Write-Host "Then open: http://localhost:4200" -ForegroundColor Yellow
Write-Host ""
