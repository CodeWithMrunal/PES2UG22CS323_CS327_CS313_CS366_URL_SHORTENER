import random
import string
import subprocess
import json
import redis
import os
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# Redis connection config from environment variables
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def get_minikube_ip():
    try:
        minikube_ip = subprocess.check_output(["minikube", "ip"]).decode("utf-8").strip()
        kubectl_output = subprocess.check_output(["kubectl", "get", "services", "url-shortener", "-o", "json"]).decode("utf-8")
        service_data = json.loads(kubectl_output)
        node_port = service_data["spec"]["ports"][0]["nodePort"]
        return f"http://{minikube_ip}:{node_port}/"
    except Exception as e:
        print(f"Error fetching Minikube IP or NodePort: {e}")
        return "http://localhost:5000/"


BASE_URL = get_minikube_ip()


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
    r.set(short_url, long_url)  # Save in Redis

    print(f"Stored {short_url} -> {long_url} in Redis")

    return jsonify({'short_url': request.host_url + short_url})


@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    long_url = r.get(short_url)
    if long_url:
        return redirect(long_url)
    return jsonify({'error': 'URL not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
