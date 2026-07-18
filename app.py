import os
import re
from flask import Flask, request, Response
import requests

app = Flask(__name__)

# دالة الاستخراج الذكي باستخدام التعبيرات النمطية (Regex)
def get_stream_url_smart(page_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(page_url, headers=headers)
        # البحث عن النمط الذي يبدأ بـ https وينتهي بـ m3u8 مع الـ token و exp
        # هذا النمط يستهدف مباشرة الرابط الذي أريتني إياه في الصورة
        pattern = r'https://[\w\.\-]+\.kora-plus\.li/live/[\w\-]+\.m3u8\?token=[\w\-]+&exp=\d+'
        match = re.search(pattern, response.text)
        
        if match:
            return match.group(0)
    except Exception:
        return None
    return None

@app.route('/stream')
def proxy_stream():
    target_url = request.args.get('url')
    
    # محاولة الاستخراج التلقائي إذا لم يرسل التطبيق رابطاً
    if not target_url:
        target_url = get_stream_url_smart("https://go4score.lc/?m=30750&lang=ar")
    
    if not target_url:
        return "فشل في جلب الرابط تلقائياً، يرجى المحاولة يدوياً عبر إرسال url", 400

    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(target_url, headers=headers, stream=True)
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
