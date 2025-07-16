from flask import Flask, request, Response, redirect
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/subscribe')
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

    allowed_headers = {
        "content-type",
        "content-disposition",
        "profile-update-interval",
        "subscription-userinfo",
        "profile-web-page-url",
        "profile-title",
    }

    try:
        response = requests.get(target_url, params=params, headers=headers)

        content = response.text
        status_code = response.status_code

        # 过滤响应头，只保留白名单里的（忽略大小写）
        filtered_headers = []
        for key, value in response.headers.items():
            if key.lower() in allowed_headers:
                filtered_headers.append((key, value))

        return Response(response=content, status=status_code, headers=filtered_headers)

    except requests.RequestException:
        return redirect('/')
