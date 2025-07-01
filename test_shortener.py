#!/usr/bin/env python3
"""
Test script for URL Shortener with Base62 encoding
"""

from url_shortener import URLShortener, Base62Encoder

def test_base62_encoding():
    """Test Base62 encoding and decoding."""
    print("=== Testing Base62 Encoding ===")
    
    test_numbers = [0, 1, 61, 62, 123, 456, 789, 1000, 999999]
    
    for num in test_numbers:
        encoded = Base62Encoder.encode(num)
        decoded = Base62Encoder.decode(encoded)
        print(f"Number: {num:6d} -> Encoded: {encoded:>6s} -> Decoded: {decoded:6d} ✓")
        assert num == decoded, f"Encoding/decoding failed for {num}"
    
    print("All Base62 tests passed! ✓\n")

def test_url_shortener():
    """Test URL shortener functionality."""
    print("=== Testing URL Shortener ===")
    
    # Initialize shortener
    shortener = URLShortener("test_urls.db")
    
    # Test URLs
    test_urls = [
        "https://www.google.com",
        "https://github.com/user/repo",
        "https://stackoverflow.com/questions/12345",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://example.com/very/long/path/to/resource?param1=value1&param2=value2"
    ]
    
    shortened_codes = []
    
    # Test shortening URLs
    print("Shortening URLs:")
    for url in test_urls:
        short_code = shortener.shorten_url(url)
        shortened_codes.append(short_code)
        print(f"Original: {url}")
        print(f"Shortened: {short_code}")
        print(f"Full short URL: http://localhost:5000/{short_code}")
        print()
    
    # Test expanding URLs
    print("Expanding URLs:")
    for i, short_code in enumerate(shortened_codes):
        expanded_url = shortener.expand_url(short_code)
        original_url = test_urls[i]
        print(f"Short code: {short_code} -> {expanded_url}")
        assert expanded_url == original_url, f"URL expansion failed for {short_code}"
    
    # Test duplicate URL handling
    print("Testing duplicate URL handling:")
    duplicate_code = shortener.shorten_url(test_urls[0])
    assert duplicate_code == shortened_codes[0], "Duplicate URL should return same short code"
    print(f"Duplicate URL correctly returned existing code: {duplicate_code}")
    
    # Test URL statistics
    print("\nURL Statistics:")
    for short_code in shortened_codes:
        stats = shortener.get_url_stats(short_code)
        if stats:
            print(f"Code: {short_code}, Clicks: {stats['click_count']}, Created: {stats['created_at']}")
    
    # Test listing all URLs
    print(f"\nTotal URLs in database: {len(shortener.list_all_urls())}")
    
    print("All URL shortener tests passed! ✓\n")

def demo_base62_characteristics():
    """Demonstrate characteristics of Base62 encoding."""
    print("=== Base62 Encoding Characteristics ===")
    
    print("Base62 alphabet:", Base62Encoder.BASE62_CHARS)
    print("Base:", Base62Encoder.BASE)
    print()
    
    print("Encoding efficiency examples:")
    examples = [
        (1, "Single digit"),
        (62, "Two digits start"),
        (3844, "Three digits start (62²)"),
        (238328, "Four digits start (62³)"),
        (14776336, "Five digits start (62⁴)")
    ]
    
    for num, description in examples:
        encoded = Base62Encoder.encode(num)
        print(f"{num:>10,} ({description:>20s}): {encoded}")
    
    print()
    print("Compared to decimal:")
    print(f"Number 1,000,000 in decimal: 1000000 (7 digits)")
    print(f"Number 1,000,000 in Base62:  {Base62Encoder.encode(1000000)} ({len(Base62Encoder.encode(1000000))} digits)")
    print()

if __name__ == "__main__":
    # Run all tests
    demo_base62_characteristics()
    test_base62_encoding()
    test_url_shortener()
    
    print("🎉 All tests completed successfully!")
    print("\nTo start the web server, run:")
    print("python app.py")
    print("\nThen visit: http://localhost:5000")
