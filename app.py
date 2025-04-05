import random
import string
import subprocess
import json
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)
url_store = {}  # In-memory dictionary to store URL mappings


def get_minikube_ip():
    """Fetch Minikube IP and the correct NodePort dynamically."""
    try:
        minikube_ip = subprocess.check_output(["minikube", "ip"]).decode("utf-8").strip()
        
        # Get the actual NodePort from kubectl
        kubectl_output = subprocess.check_output(["kubectl", "get", "services", "url-shortener", "-o", "json"]).decode("utf-8")
        service_data = json.loads(kubectl_output)
        node_port = service_data["spec"]["ports"][0]["nodePort"]  # Fetch dynamically

        return f"http://{minikube_ip}:{node_port}/"
    except Exception as e:
        print(f"Error fetching Minikube IP or NodePort: {e}")
        return "http://localhost:5000/"  # Fallback for local testing


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
    url_store[short_url] = long_url

    print(f"Stored {short_url} -> {long_url} in memory")

    return jsonify({'short_url': request.host_url + short_url})  # dynamically returns host URL



@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    long_url = url_store.get(short_url)
    if long_url:
        return redirect(long_url)
    return jsonify({'error': 'URL not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
