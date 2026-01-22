# Test Upload Endpoint Response
Write-Host "Testing upload endpoint response structure..." -ForegroundColor Cyan

# Create a simple test file
$testFile = "test-upload.txt"
"This is a test document for upload." | Out-File -FilePath $testFile -Encoding UTF8

# Test the upload
try {
    Write-Host "`nUploading file via API..." -ForegroundColor Yellow
    
    # Use curl to properly test multipart/form-data
    $response = curl.exe -X POST http://localhost:4200/api/upload `
        -F "file=@$testFile" `
        -H "Accept: application/json" `
        --silent --show-error --write-out "`n%{http_code}"
    
    Write-Host "`nRaw Response:" -ForegroundColor Cyan
    Write-Host $response -ForegroundColor White
    
    # Parse JSON from response
    $lines = $response -split "`n"
    $statusCode = $lines[-1]
    $jsonResponse = ($lines[0..($lines.Length-2)] -join "`n")
    
    Write-Host "`nStatus Code: $statusCode" -ForegroundColor $(if ($statusCode -eq "200") { "Green" } else { "Red" })
    
    if ($jsonResponse) {
        Write-Host "JSON Response:" -ForegroundColor Cyan
        $json = $jsonResponse | ConvertFrom-Json
        $json | ConvertTo-Json -Depth 5
        
        Write-Host "`nResponse Fields:" -ForegroundColor Cyan
        Write-Host "  success: $($json.success)" -ForegroundColor White
        Write-Host "  document_id: $($json.document_id)" -ForegroundColor White
        Write-Host "  filename: $($json.filename)" -ForegroundColor White
        Write-Host "  message: $($json.message)" -ForegroundColor White
        if ($json.error) {
            Write-Host "  error: $($json.error)" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
} finally {
    # Clean up
    if (Test-Path $testFile) {
        Remove-Item $testFile
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Check Backend Terminal for Logs" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan
