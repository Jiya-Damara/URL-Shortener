Write-Host "Starting URL Shortener with Base62 Encoding..." -ForegroundColor Green
Write-Host "Navigate to http://localhost:5000 in your browser" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host ""

try {
    python app.py
} catch {
    Write-Host "Error starting the application. Make sure Flask is installed:" -ForegroundColor Red
    Write-Host "pip install flask" -ForegroundColor Yellow
}

Read-Host "Press Enter to exit"
