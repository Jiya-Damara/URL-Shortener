@echo off
echo.
echo 🔗 URL Shortener with Base62 Encoding
echo =====================================
echo.

echo 📋 Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

echo.
echo 📦 Installing dependencies...
pip install flask gunicorn
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✅ Testing the application...
python test_shortener.py
if %errorlevel% neq 0 (
    echo ❌ Tests failed
    pause
    exit /b 1
)

echo.
echo 🚀 Starting URL Shortener web server...
echo.
echo 🌐 Open your browser and go to: http://localhost:5000
echo 📱 Or try the demo: python demo.py
echo 🛑 Press Ctrl+C to stop the server
echo.

python app.py

echo.
echo 👋 Server stopped. Press any key to exit...
pause > nul
