from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/sub')
def sub():
    token = request.args.get('token')
    flag = request.args.get('flag')

    if not token:
        return jsonify({'error': 'Missing required parameter: token'}), 400

    target_url = 'https://server.metc.uk/sub.php'
    params = {'token': token}
    if flag:
        params['flag'] = flag

    headers = {}
    for key, value in request.headers:
        headers[key] = value

    try:
        response = requests.get(target_url, params=params, headers=headers)
        return (response.content, response.status_code, response.headers.items())
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
