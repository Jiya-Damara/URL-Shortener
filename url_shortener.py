import string
import sqlite3
from datetime import datetime

class Base62Encoder:
    """
    Base62 encoding utility for URL shortening.
    Uses alphanumeric characters (0-9, a-z, A-Z) for encoding.
    """
    
    BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase
    BASE = 62
    
    @classmethod
    def encode(cls, num):
        """Convert a number to base62 string."""
        if num == 0:
            return cls.BASE62_CHARS[0]
        
        encoded = ""
        while num > 0:
            encoded = cls.BASE62_CHARS[num % cls.BASE] + encoded
            num //= cls.BASE
        return encoded
    
    @classmethod
    def decode(cls, encoded_str):
        """Convert a base62 string back to number."""
        num = 0
        for char in encoded_str:
            num = num * cls.BASE + cls.BASE62_CHARS.index(char)
        return num

class URLShortener:
    """
    URL Shortener class that handles the core logic for shortening and expanding URLs.
    """
    
    def __init__(self, db_path="urls.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_code TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                click_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def shorten_url(self, original_url):
        """
        Shorten a URL and return the short code.
        
        Args:
            original_url (str): The original URL to shorten
            
        Returns:
            str: The base62 encoded short code
        """
        # Check if URL already exists
        existing_code = self.get_existing_short_code(original_url)
        if existing_code:
            return existing_code
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert the URL and get the auto-generated ID
        cursor.execute(
            "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
            (original_url, "temp")
        )
        
        url_id = cursor.lastrowid
        
        # Generate base62 encoded short code
        short_code = Base62Encoder.encode(url_id)
        
        # Update the record with the actual short code
        cursor.execute(
            "UPDATE urls SET short_code = ? WHERE id = ?",
            (short_code, url_id)
        )
        
        conn.commit()
        conn.close()
        
        return short_code
    
    def get_existing_short_code(self, original_url):
        """Check if URL already exists and return its short code."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT short_code FROM urls WHERE original_url = ?",
            (original_url,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def expand_url(self, short_code):
        """
        Expand a short code back to the original URL.
        
        Args:
            short_code (str): The base62 encoded short code
            
        Returns:
            str: The original URL, or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT original_url FROM urls WHERE short_code = ?",
            (short_code,)
        )
        
        result = cursor.fetchone()
        
        if result:
            # Increment click count
            cursor.execute(
                "UPDATE urls SET click_count = click_count + 1 WHERE short_code = ?",
                (short_code,)
            )
            conn.commit()
        
        conn.close()
        
        return result[0] if result else None
    
    def get_url_stats(self, short_code):
        """Get statistics for a shortened URL."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT original_url, created_at, click_count FROM urls WHERE short_code = ?",
            (short_code,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'original_url': result[0],
                'created_at': result[1],
                'click_count': result[2]
            }
        return None
    
    def list_all_urls(self):
        """List all shortened URLs."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT short_code, original_url, created_at, click_count FROM urls ORDER BY created_at DESC"
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'short_code': row[0],
                'original_url': row[1],
                'created_at': row[2],
                'click_count': row[3]
            }
            for row in results
        ]
