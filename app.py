@app.route('/stream')
def proxy_stream():
    target_url = request.args.get('url')
    if not target_url:
        return "يجب توفير الرابط", 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Referer': 'https://go4score.lc/',
        'Origin': 'https://go4score.lc/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # إرسال الطلب مع تعطيل التتبع التلقائي للتأكد من أننا نتحكم في المسار
        req = requests.get(target_url, headers=headers, stream=True, allow_redirects=True)
        
        # إذا كان الموقع لا يزال يحاول توجيهنا، سنقوم بإيقاف الطلب فوراً
        if "google.com" in req.url:
            return "الموقع رفض الطلب وقام بتحويلنا لجوجل. نحتاج لتعديل الهيدرز.", 403
            
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
