import os
from flask import Flask, Response
import requests

app = Flask(__name__)

# رابط اختبار لضمان عمل السيرفر (يمكنك تغييره لاحقاً)
STREAM_SOURCE = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8" 

@app.route('/stream')
def proxy_stream():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        # طلب البيانات من المصدر
        response = requests.get(STREAM_SOURCE, headers=headers, stream=True)
        # تمرير البيانات للمستخدم
        return Response(response.iter_content(chunk_size=1024), 
                        content_type=response.headers.get('Content-Type', 'application/x-mpegURL'))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Render يعطينا المنفذ تلقائياً، أو نستخدم 10000 كافتراضي
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)