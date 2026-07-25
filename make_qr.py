#!/usr/bin/env python3
"""Generate QR code for the study app URL."""
import qrcode

url = 'https://a06244d97c3c877f-112-112-42-107.serveousercontent.com'

qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')

out = r'C:\Users\Administrator\Desktop\二建备考\qrcode.png'
img.save(out)
print(f'QR code saved to: {out}')
print(f'URL: {url}')
