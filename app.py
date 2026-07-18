import os
from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/stream')
def proxy_stream():
    # استقبال الرابط المحدث من تطبيقك
    target_url = request.args.get('url')
    
    if not target_url:
        return "يرجى إرسال رابط البث المحدث عبر معامل ?url=...", 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://go4score.lc/' # ضروري جداً لتمويه الموقع بأنك قادم منه
    }
    
    try:
        # إضافة allow_redirects=True لمتابعة الرابط الأصلي للفيديو وتجاوز إعادة التوجيه
        response = requests.get(target_url, headers=headers, stream=True, allow_redirects=True)
        
        return Response(
            response.iter_content(chunk_size=1024), 
            content_type=response.headers.get('Content-Type', 'application/x-mpegURL'),
            status=response.status_code
        )
    except Exception as e:
        return f"خطأ في البروكسي: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
