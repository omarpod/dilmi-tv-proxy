import os
import re
import requests
from flask import Flask, request, Response

app = Flask(__name__)

def get_stream_url_smart(page_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        session = requests.Session()
        # زيارة الصفحة الرئيسية للحصول على الكوكيز والملفات
        response = session.get(page_url, headers=headers)
        
        # البحث عن ملفات الجافا سكريبت التي قد تحتوي على الرابط
        script_files = re.findall(r'src=["\'](https://[\w\.\-/]+\.js)["\']', response.text)
        
        # نمط البحث عن الرابط
        pattern = r'https://[\w\.\-]+\.kora-plus\.li/live/[\w\-]+\.m3u8\?token=[\w\-]+&exp=\d+'
        
        # 1. البحث في الصفحة الرئيسية أولاً
        match = re.search(pattern, response.text)
        if match: return match.group(0)
        
        # 2. البحث في ملفات الجافا سكريبت إذا لم نجد الرابط في الصفحة
        for js_url in script_files:
            js_response = session.get(js_url, headers=headers)
            match = re.search(pattern, js_response.text)
            if match: return match.group(0)
            
    except Exception:
        return None
    return None

@app.route('/stream')
def proxy_stream():
    target_url = request.args.get('url')
    if not target_url:
        target_url = get_stream_url_smart("https://go4score.lc/?m=30750&lang=ar")
    
    if not target_url:
        return "فشل الاستخراج التلقائي. يرجى التأكد من أن الرابط لا يزال متاحاً في المصدر.", 404

    try:
        # إرسال الطلب للمصدر مع إظهارنا كمتصفح شرعي
        resp = requests.get(target_url, headers={'User-Agent': 'Mozilla/5.0'}, stream=True)
        return Response(resp.iter_content(chunk_size=1024), 
                        content_type=resp.headers.get('Content-Type', 'application/x-mpegURL'),
                        status=resp.status_code)
    except Exception as e:
        return f"خطأ: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
