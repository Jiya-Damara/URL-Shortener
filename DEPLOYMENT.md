# 🚀 How to Run and Deploy Your URL Shortener

## 🏃‍♂️ Quick Start (Local Development)

### Method 1: Simple Run
```bash
# Navigate to your project folder
cd "c:\Users\HP\Desktop\URL_shortener"

# Install dependencies
pip install flask

# Run the application
python app.py
```

### Method 2: Use Startup Scripts
**Option A - Batch File (Windows):**
- Double-click `start.bat`

**Option B - PowerShell:**
```powershell
.\start.ps1
```

### Method 3: Test First, Then Run
```bash
# Test the Base62 encoding
python test_shortener.py

# Try interactive demo
python demo.py

# Start web server
python app.py
```

**🌐 Then visit:** http://localhost:5000

---

## 🔧 Local Development Setup

### 1. Prerequisites
- Python 3.7+ installed
- pip package manager

### 2. Environment Setup
```bash
# Create virtual environment (recommended)
python -m venv url_shortener_env

# Activate virtual environment
# Windows:
url_shortener_env\Scripts\activate
# Mac/Linux:
source url_shortener_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Development Server
```bash
python app.py
```

**Features available:**
- 🏠 **Home:** http://localhost:5000
- 📋 **URL List:** http://localhost:5000/list
- 🔗 **Short URLs:** http://localhost:5000/{code}
- 📊 **API:** http://localhost:5000/api/list

---

## 🌐 Production Deployment Options

### Option 1: Heroku (Easiest Cloud Deployment)

#### Step 1: Prepare for Heroku
```bash
# Install Heroku CLI first from https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create Heroku app
heroku create your-url-shortener-name
```

#### Step 2: Create Heroku Files
Create `Procfile`:
```
web: gunicorn app:app
```

Update `requirements.txt`:
```
Flask==2.3.3
gunicorn==21.2.0
```

#### Step 3: Deploy
```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Deploy to Heroku
git push heroku main
```

**Your app will be at:** https://your-url-shortener-name.herokuapp.com

### Option 2: Railway (Modern Alternative)

#### Step 1: Prepare Railway Files
Create `railway.toml`:
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "gunicorn app:app"
```

#### Step 2: Deploy
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway deploy
```

### Option 3: Render (Free Tier Available)

#### Step 1: Create `render.yaml`
```yaml
services:
  - type: web
    name: url-shortener
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

#### Step 2: Connect to GitHub and Deploy
- Push to GitHub
- Connect Render to your GitHub repo
- Auto-deploy on push

### Option 4: VPS/Server Deployment

#### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Create application directory
sudo mkdir /var/www/url-shortener
sudo chown $USER:$USER /var/www/url-shortener
```

#### Step 2: Application Setup
```bash
# Upload your files to /var/www/url-shortener
cd /var/www/url-shortener

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

#### Step 3: Systemd Service
Create `/etc/systemd/system/url-shortener.service`:
```ini
[Unit]
Description=URL Shortener
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/url-shortener
Environment="PATH=/var/www/url-shortener/venv/bin"
ExecStart=/var/www/url-shortener/venv/bin/gunicorn --workers 3 --bind unix:url-shortener.sock -m 007 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Step 4: Nginx Configuration
Create `/etc/nginx/sites-available/url-shortener`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/url-shortener/url-shortener.sock;
    }
}
```

#### Step 5: Enable and Start
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/url-shortener /etc/nginx/sites-enabled

# Start services
sudo systemctl enable url-shortener
sudo systemctl start url-shortener
sudo systemctl restart nginx
```

---

## 🔧 Configuration for Production

### 1. Update `app.py` for Production
```python
# Change debug mode
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

### 2. Environment Variables
```python
import os

# Use environment variables for sensitive data
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# Database path
db_path = os.environ.get('DATABASE_PATH', 'urls.db')
```

### 3. Security Headers
```python
from flask import Flask

@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

---

## 📊 Monitoring and Maintenance

### 1. Logs
```bash
# Check application logs
sudo journalctl -u url-shortener -f

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### 2. Database Backup
```python
# Create backup script
import sqlite3
import shutil
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy('urls.db', f'backup_urls_{timestamp}.db')
```

### 3. Health Check Endpoint
Add to `app.py`:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

---

## 🚨 Troubleshooting

### Common Issues:

1. **Port already in use:**
   ```bash
   # Change port in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. **Flask not found:**
   ```bash
   pip install flask
   ```

3. **Permission errors:**
   ```bash
   # Run with administrator privileges
   # Or check file permissions
   ```

4. **Database locked:**
   ```python
   # Ensure database connections are properly closed
   # Check url_shortener.py for proper conn.close()
   ```

---

## 🔐 Security Checklist

- [ ] Change default secret key
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Use environment variables for secrets
- [ ] Regular database backups
- [ ] Monitor for abuse
- [ ] Set up proper logging

---

## 📈 Scaling Considerations

### For High Traffic:
1. **Use Redis for caching**
2. **Implement connection pooling**
3. **Add rate limiting**
4. **Use CDN for static files**
5. **Consider database optimization**
6. **Implement horizontal scaling**

Your URL shortener is now ready for both development and production use! 🎉
