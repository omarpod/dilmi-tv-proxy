import os
from flask import Flask, request, Response
import requests

app = Flask(__name__)

# إنشاء جلسة دائمة للحفاظ على الكوكيز
session = requests.Session()

@app.route('/stream')
def proxy_stream():
    target_url = request.args.get('url')
    if not target_url:
        return "يجب توفير الرابط", 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Referer': 'https://go4score.lc/',
        'Origin': 'https://go4score.lc/',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }
    
    try:
        # 1. زيارة الصفحة الرئيسية أولاً لتسجيل الجلسة
        session.get('https://go4score.lc/', headers=headers)
        
        # 2. طلب ملف الفيديو باستخدام الجلسة المحملة بالكوكيز
        req = session.get(target_url, headers=headers, stream=True, allow_redirects=True)
        
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
