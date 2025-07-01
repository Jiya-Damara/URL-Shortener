from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import re
import os
from url_shortener import URLShortener

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Initialize URL shortener
shortener = URLShortener()

def is_valid_url(url):
    """Validate URL format."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

@app.route('/')
def index():
    """Home page with URL shortening form."""
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    """API endpoint to shorten a URL."""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        original_url = data['url'].strip()
        
        # Add http:// if no protocol specified
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url
        
        # Validate URL
        if not is_valid_url(original_url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Shorten the URL
        short_code = shortener.shorten_url(original_url)
        short_url = request.host_url + short_code
        
        return jsonify({
            'original_url': original_url,
            'short_url': short_url,
            'short_code': short_code
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/expand/<short_code>')
def expand(short_code):
    """API endpoint to get original URL from short code."""
    try:
        original_url = shortener.expand_url(short_code)
        
        if original_url:
            return jsonify({
                'original_url': original_url,
                'short_code': short_code
            })
        else:
            return jsonify({'error': 'Short URL not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect short code to original URL."""
    try:
        original_url = shortener.expand_url(short_code)
        
        if original_url:
            return redirect(original_url)
        else:
            flash('Short URL not found', 'error')
            return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/stats/<short_code>')
def stats(short_code):
    """Get statistics for a short URL."""
    try:
        stats_data = shortener.get_url_stats(short_code)
        
        if stats_data:
            return jsonify(stats_data)
        else:
            return jsonify({'error': 'Short URL not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list')
def list_urls():
    """List all shortened URLs."""
    try:
        urls = shortener.list_all_urls()
        return render_template('list.html', urls=urls)
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/list')
def api_list_urls():
    """API endpoint to list all shortened URLs."""
    try:
        urls = shortener.list_all_urls()
        return jsonify(urls)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment (for deployment platforms)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
