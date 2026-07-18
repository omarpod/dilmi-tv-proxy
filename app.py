import os
from flask import Flask, request, Response
import requests

# 1. التعريف يجب أن يكون في البداية
app = Flask(__name__)

# 2. ثم الدوال
@app.route('/stream')
def proxy_stream():
    target_url = request.args.get('url')
    if not target_url:
        return "يجب توفير الرابط", 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Referer': 'https://go4score.lc/',
        'Origin': 'https://go4score.lc/'
    }
    
    try:
        req = requests.get(target_url, headers=headers, stream=True, allow_redirects=True)
        return Response(
            req.iter_content(chunk_size=1024),
            status=req.status_code,
            headers={
                'Content-Type': req.headers.get('Content-Type', 'application/x-mpegURL'),
                'Access-Control-Allow-Origin': '*'
            }
        )
    except Exception as e:
        return str(e), 500

# 3. التشغيل في النهاية
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
