# URL Shortener with Base62 Encoding

A simple yet powerful URL shortener built with Python, Flask, and SQLite, featuring Base62 encoding for compact short URLs.

## Features

- ✨ **Base62 Encoding**: Uses alphanumeric characters (0-9, a-z, A-Z) for shortest possible URLs
- 🌐 **Web Interface**: Clean, modern web UI for shortening URLs
- 📊 **Click Tracking**: Tracks how many times each short URL is accessed
- 🔗 **REST API**: Full API support for programmatic access
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🗄️ **SQLite Database**: Persistent storage with no setup required
- 🔍 **URL Validation**: Ensures only valid URLs are shortened
- 📋 **URL Management**: View all shortened URLs with statistics

## How Base62 Encoding Works

Base62 encoding uses 62 characters: `0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`

**Benefits:**
- **Compact**: Much shorter than decimal numbers
- **URL-safe**: All characters are safe for URLs
- **Case-sensitive**: Maximizes character space
- **Human-readable**: Easy to type and share

**Examples:**
- ID 1 → `1`
- ID 62 → `10` 
- ID 1000 → `g8`
- ID 1,000,000 → `4c92`

## Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install flask
   ```
3. **Run the application**:
   ```bash
   python app.py
   ```
4. **Visit** http://localhost:5000

## Usage

### Web Interface

1. Open http://localhost:5000 in your browser
2. Enter a URL to shorten
3. Copy the generated short URL
4. View all URLs at http://localhost:5000/list

### API Endpoints

#### Shorten a URL
```bash
POST /shorten
Content-Type: application/json

{
    "url": "https://example.com"
}
```

**Response:**
```json
{
    "original_url": "https://example.com",
    "short_url": "http://localhost:5000/1",
    "short_code": "1"
}
```

#### Expand a URL
```bash
GET /expand/<short_code>
```

**Response:**
```json
{
    "original_url": "https://example.com",
    "short_code": "1"
}
```

#### Get URL Statistics
```bash
GET /stats/<short_code>
```

**Response:**
```json
{
    "original_url": "https://example.com",
    "created_at": "2025-07-01 12:00:00",
    "click_count": 5
}
```

#### List All URLs
```bash
GET /api/list
```

#### Redirect (Access Short URL)
```bash
GET /<short_code>
```
Redirects to the original URL and increments click counter.

## Project Structure

```
URL_shortener/
├── app.py                 # Flask web application
├── url_shortener.py       # Core URL shortener logic with Base62
├── test_shortener.py      # Test script and demonstrations
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Main page template
│   └── list.html         # URL list template
└── README.md             # This file
```

## Testing

Run the test script to see Base62 encoding in action:

```bash
python test_shortener.py
```

This will:
- Demonstrate Base62 encoding characteristics
- Test encoding/decoding with various numbers
- Test URL shortening and expansion
- Show click tracking functionality

## Database Schema

The SQLite database (`urls.db`) contains a single table:

```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
    short_code TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    click_count INTEGER DEFAULT 0
);
```

## Configuration

### Production Deployment

1. **Change the secret key** in `app.py`:
   ```python
   app.secret_key = 'your-secure-random-secret-key'
   ```

2. **Set Flask environment**:
   ```bash
   export FLASK_ENV=production
   ```

3. **Use a production WSGI server** like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

### Customization

- **Domain**: Update the `request.host_url` references for custom domains
- **Database**: Modify `URLShortener.__init__()` to use a different database path
- **Base62 alphabet**: Customize `Base62Encoder.BASE62_CHARS` if needed

## Technical Details

### Base62 Implementation

The Base62 encoder converts decimal numbers to a base-62 representation:

```python
def encode(cls, num):
    if num == 0:
        return cls.BASE62_CHARS[0]
    
    encoded = ""
    while num > 0:
        encoded = cls.BASE62_CHARS[num % cls.BASE] + encoded
        num //= cls.BASE
    return encoded
```

### URL Shortening Process

1. **URL Validation**: Check if URL format is valid
2. **Duplicate Check**: Return existing short code if URL already exists
3. **Database Insert**: Insert URL into database, get auto-increment ID
4. **Base62 Encoding**: Convert database ID to Base62 string
5. **Update Record**: Store the Base62 code back to database

### Security Considerations

- **URL Validation**: Prevents malicious URLs from being shortened
- **SQL Injection**: Uses parameterized queries
- **Rate Limiting**: Consider adding rate limiting for production use
- **HTTPS**: Use HTTPS in production for secure transmission

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Future Enhancements

- [ ] Custom short codes
- [ ] Expiration dates for URLs
- [ ] Rate limiting
- [ ] User accounts and URL management
- [ ] Analytics dashboard
- [ ] QR code generation
- [ ] Bulk URL shortening
- [ ] API authentication
