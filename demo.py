#!/usr/bin/env python3
"""
Demo script showing URL Shortener capabilities
"""

import time
import threading
import webbrowser
from url_shortener import URLShortener, Base62Encoder

def demo_console_interface():
    """Interactive console demo of the URL shortener."""
    print("🔗 URL Shortener with Base62 Encoding - Interactive Demo")
    print("=" * 60)
    
    shortener = URLShortener("demo_urls.db")
    
    while True:
        print("\nOptions:")
        print("1. Shorten a URL")
        print("2. Expand a short code")
        print("3. View URL statistics")
        print("4. List all URLs")
        print("5. Base62 encoding demo")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            url = input("Enter URL to shorten: ").strip()
            if url:
                try:
                    if not url.startswith(('http://', 'https://')):
                        url = 'http://' + url
                    short_code = shortener.shorten_url(url)
                    print(f"✅ Shortened URL: http://localhost:5000/{short_code}")
                    print(f"   Short code: {short_code}")
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        elif choice == "2":
            short_code = input("Enter short code: ").strip()
            if short_code:
                original_url = shortener.expand_url(short_code)
                if original_url:
                    print(f"✅ Original URL: {original_url}")
                else:
                    print("❌ Short code not found")
        
        elif choice == "3":
            short_code = input("Enter short code: ").strip()
            if short_code:
                stats = shortener.get_url_stats(short_code)
                if stats:
                    print(f"📊 Statistics for {short_code}:")
                    print(f"   Original URL: {stats['original_url']}")
                    print(f"   Created: {stats['created_at']}")
                    print(f"   Clicks: {stats['click_count']}")
                else:
                    print("❌ Short code not found")
        
        elif choice == "4":
            urls = shortener.list_all_urls()
            if urls:
                print(f"\n📋 All URLs ({len(urls)} total):")
                print("-" * 80)
                for url in urls:
                    print(f"Code: {url['short_code']:>6s} | Clicks: {url['click_count']:>3d} | {url['original_url']}")
            else:
                print("📭 No URLs in database")
        
        elif choice == "5":
            print("\n🔢 Base62 Encoding Demo:")
            print(f"Alphabet: {Base62Encoder.BASE62_CHARS}")
            print(f"Base: {Base62Encoder.BASE}")
            print("\nExamples:")
            examples = [1, 62, 123, 456, 3844, 1000000]
            for num in examples:
                encoded = Base62Encoder.encode(num)
                print(f"  {num:>8,} → {encoded}")
        
        elif choice == "6":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    print("Welcome to the URL Shortener Demo!")
    print("\nThis demo includes:")
    print("✓ Base62 encoding for compact URLs")
    print("✓ SQLite database for persistence")  
    print("✓ Click tracking and statistics")
    print("✓ Web interface (run 'python app.py' separately)")
    print("\nStarting console demo...")
    time.sleep(2)
    
    try:
        demo_console_interface()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your installation and try again.")
