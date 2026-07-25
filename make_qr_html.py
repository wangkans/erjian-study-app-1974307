#!/usr/bin/env python3
"""Generate QR code without PIL - output as HTML with canvas."""
import base64

url = 'https://a06244d97c3c877f-112-112-42-107.serveousercontent.com'

html = '''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>扫码打开题库</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{display:flex;justify-content:center;align-items:center;min-height:100vh;background:#f5f5f5;font-family:sans-serif;margin:0}
.card{background:#fff;border-radius:16px;padding:30px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.1)}
h2{margin:0 0 10px;color:#2b6cb0}
p{color:#718096;font-size:14px;margin:10px 0}
#qr{margin:20px auto;width:256px;height:256px}
.btn{display:inline-block;padding:12px 24px;background:#2b6cb0;color:#fff;border-radius:8px;text-decoration:none;font-size:16px;margin-top:10px}
</style></head><body>
<div class="card">
<h2>📚 二建备考题库</h2>
<p>用手机相机/微信扫码打开</p>
<div id="qr"></div>
<a class="btn" href="''' + url + '''" target="_blank">点此打开</a>
<p style="font-size:12px;margin-top:15px;word-break:break-all">''' + url + '''</p>
</div>
<script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>
<script>new QRCode(document.getElementById("qr"),{text:"''' + url + '''",width:256,height:256});</script>
</body></html>'''

path = r'C:\Users\Administrator\Desktop\二建备考\scan_qr.html'
with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'QR page saved to: {path}')
print(f'Open in browser to scan QR code with phone')
