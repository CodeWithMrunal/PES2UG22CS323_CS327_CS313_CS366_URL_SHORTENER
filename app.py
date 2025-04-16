from flask import Flask, request, jsonify, redirect, send_from_directory
import redis
from pymongo import MongoClient
import random
import string
import os

app = Flask(__name__, static_folder='static')

# Redis setup (for caching)
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis-service')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# MongoDB setup (for persistence)
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongodb-service')
MONGO_PORT = int(os.environ.get('MONGO_PORT', 27017))
mongo_client = MongoClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}/')
db = mongo_client.url_shortener
urls_collection = db.urls

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url')
    
    if not long_url:
        return jsonify({'error': 'URL is required'}), 400

    # Generate short URL
    short_url = generate_short_url()
    
    # Store in both Redis and MongoDB
    redis_client.set(short_url, long_url)
    urls_collection.insert_one({
        'short_url': short_url,
        'long_url': long_url
    })
    
    return jsonify({'short_url': request.host_url + short_url})

@app.route('/<short_url>')
def redirect_url(short_url):
    # Try Redis first (faster)
    long_url = redis_client.get(short_url)
    
    if long_url:
        return redirect(long_url.decode('utf-8'))
    
    # If not in Redis, check MongoDB
    url_mapping = urls_collection.find_one({'short_url': short_url})
    if url_mapping:
        # Store in Redis for future use
        redis_client.set(short_url, url_mapping['long_url'])
        return redirect(url_mapping['long_url'])
    
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)