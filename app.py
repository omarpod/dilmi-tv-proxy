@app.route('/stream')
def proxy_stream():
    target_url = request.args.get('url')
    if not target_url:
        return "يجب توفير الرابط", 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Referer': 'https://go4score.lc/',
        # إضافة هذه الكوكيز يخدع الموقع بأن الطلب قادم من متصفح لديه الخدمة
        'Cookie': 'ss_vid=1; session_id=live_stream_active' 
    }
    
    try:
        req = requests.get(target_url, headers=headers, stream=True, allow_redirects=False)
        
        # إذا حاول الموقع تحويلنا (302)، سنأخذ الرابط الجديد ونحاول مرة واحدة فقط
        if req.status_code in [301, 302, 307, 308]:
            new_url = req.headers.get('Location')
            req = requests.get(new_url, headers=headers, stream=True)

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
