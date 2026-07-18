import os
from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# دالة الاستخراج الذكي
def get_stream_url_from_site(page_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # هنا نبحث عن الرابط الذي يحتوي على m3u8
    # ملاحظة: هذا المسار يعتمد على هيكلية الموقع الذي أريتني إياه
    scripts = soup.find_all('script')
    for script in scripts:
        if 'm3u8' in str(script):
            # الكود هنا يحتاج تخصيص بناءً على موقعك، 
            # لكن هذا هو المسار العام للمحترفين
            return "رابط_البث_المستخرج_مؤقتاً"
    return None

@app.route('/stream')
def proxy_stream():
    target_url = request.args.get('url')
    
    # إذا لم يرسل التطبيق رابطاً، جرب استخراجه تلقائياً
    if not target_url:
        target_url = get_stream_url_from_site("https://go4score.lc/?m=30750&lang=ar")
    
    if not target_url:
        return "فشل في جلب الرابط، يرجى المحاولة يدوياً", 400

    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(target_url, headers=headers, stream=True)
        return Response(
            response.iter_content(chunk_size=1024), 
            content_type=response.headers.get('Content-Type', 'application/x-mpegURL'),
            status=response.status_code
        )
    except Exception as e:
        return f"خطأ: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
