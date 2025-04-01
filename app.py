import random
import string
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)
url_store = {}  # In-memory dictionary to store URL mappings

BASE_URL = "http://localhost:5000/"

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/')
def test():
    return 'Server is working!'

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url')
    if not long_url:
        return jsonify({'error': 'URL is required'}), 400
    
    short_url = generate_short_url()
    url_store[short_url] = long_url  # Store in dictionary
    
    print(f"Stored {short_url} -> {long_url} in memory")  # Logging
    
    return jsonify({'short_url': BASE_URL + short_url})

@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    long_url = url_store.get(short_url)
    if long_url:
        return redirect(long_url)
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
