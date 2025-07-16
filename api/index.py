from flask import Flask, request, Response, redirect
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
        return redirect('/')

    target_url = 'https://sub.metc.uk'
    params = {'token': token}
    if flag:
        params['flag'] = flag

    user_agent = request.headers.get('User-Agent', '')
    headers = {'User-Agent': user_agent} if user_agent else {}

    try:
        response = requests.get(target_url, params=params, headers=headers)
        content = response.text
        status_code = response.status_code
        content_type = response.headers.get('Content-Type', 'text/plain')
        return Response(content, status=status_code, content_type=content_type)
    except requests.RequestException as e:
        return redirect('/')
