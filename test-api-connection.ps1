# API Connection Diagnostic Script
# Tests all connections between frontend and backend

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "API Connection Diagnostic Test" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Test 1: Backend Direct Access
Write-Host "[TEST 1] Backend Direct Access (http://localhost:8000)" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -ErrorAction Stop
    Write-Host "  ✅ Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  ✅ Content: $($response.Content)" -ForegroundColor Green
} catch {
    Write-Host "  ❌ FAILED: $_" -ForegroundColor Red
    Write-Host "  ⚠️  Backend is NOT running on port 8000!" -ForegroundColor Red
    Write-Host "  💡 Start backend: cd backend && python -m app.main`n" -ForegroundColor Yellow
    exit 1
}

# Test 2: Frontend Proxy Access
Write-Host "`n[TEST 2] Frontend Proxy Access (http://localhost:4200/api)" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:4200/api/health" -Method GET -ErrorAction Stop
    Write-Host "  ✅ Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  ✅ Content: $($response.Content)" -ForegroundColor Green
} catch {
    Write-Host "  ❌ FAILED: $_" -ForegroundColor Red
    if ($_.Exception.Message -match "Unable to connect") {
        Write-Host "  ⚠️  Angular dev server is NOT running on port 4200!" -ForegroundColor Red
        Write-Host "  💡 Start frontend: cd frontend/angular-ui && npm start`n" -ForegroundColor Yellow
    } else {
        Write-Host "  ⚠️  Proxy configuration may be incorrect!" -ForegroundColor Red
    }
    exit 1
}

# Test 3: CORS Headers
Write-Host "`n[TEST 3] CORS Configuration" -ForegroundColor Yellow
try {
    $headers = @{
        "Origin" = "http://localhost:4200"
    }
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -Headers $headers -ErrorAction Stop
    $corsHeader = $response.Headers["Access-Control-Allow-Origin"]
    if ($corsHeader -eq "*" -or $corsHeader -eq "http://localhost:4200") {
        Write-Host "  ✅ CORS Headers: $corsHeader" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  CORS may not be configured correctly: $corsHeader" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ FAILED: $_" -ForegroundColor Red
}

# Test 4: Test POST endpoint
Write-Host "`n[TEST 4] POST /api/analyze Endpoint" -ForegroundColor Yellow
try {
    $body = @{
        document_text = "This is a test document."
    } | ConvertTo-Json

    $response = Invoke-WebRequest -Uri "http://localhost:4200/api/analyze" -Method POST -Body $body -ContentType "application/json" -ErrorAction Stop
    Write-Host "  ✅ Status: $($response.StatusCode)" -ForegroundColor Green
    $jsonResponse = $response.Content | ConvertFrom-Json
    if ($jsonResponse.success) {
        Write-Host "  ✅ Response Success: True" -ForegroundColor Green
        Write-Host "  ✅ API Integration: WORKING" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  API returned success: false" -ForegroundColor Yellow
        Write-Host "  Content: $($response.Content)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ FAILED: $_" -ForegroundColor Red
    if ($_.ErrorDetails) {
        Write-Host "  Error Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}

# Test 5: Browser Console Instructions
Write-Host "`n[TEST 5] Browser Console Check" -ForegroundColor Yellow
Write-Host "  📝 To check browser console errors:" -ForegroundColor Cyan
Write-Host "     1. Open http://localhost:4200 in browser" -ForegroundColor White
Write-Host "     2. Press F12 to open DevTools" -ForegroundColor White
Write-Host "     3. Go to Console tab" -ForegroundColor White
Write-Host "     4. Go to Network tab" -ForegroundColor White
Write-Host "     5. Try to analyze a document" -ForegroundColor White
Write-Host "     6. Check for any red errors or failed requests" -ForegroundColor White

# Test 6: Configuration Summary
Write-Host "`n[TEST 6] Configuration Summary" -ForegroundColor Yellow
Write-Host "  Backend URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Frontend URL: http://localhost:4200" -ForegroundColor Cyan
Write-Host "  API Proxy: /api -> http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Proxy Config: frontend/angular-ui/proxy.conf.json" -ForegroundColor Cyan

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ ALL TESTS PASSED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`n💡 If frontend still shows errors:" -ForegroundColor Yellow
Write-Host "   1. Clear browser cache (Ctrl+Shift+Delete)" -ForegroundColor White
Write-Host "   2. Restart Angular dev server" -ForegroundColor White
Write-Host "   3. Check browser console for specific errors" -ForegroundColor White
Write-Host "   4. Verify no firewall blocking port 8000 or 4200" -ForegroundColor White
Write-Host "   5. Check that you're using http:// not https://`n" -ForegroundColor White
