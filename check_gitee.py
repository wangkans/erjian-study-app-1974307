#!/usr/bin/env python3
"""Check Gitee repository settings page for Pages option."""
import urllib.request, re, ssl

ctx = ssl.create_default_context()
TOKEN = '5c2afd33f8b65f43424e1a494f045892'

req = urllib.request.Request(
    'https://gitee.com/wang7f/erjian-study/settings',
    headers={
        'User-Agent': 'Mozilla/5.0',
        'Cookie': 'access_token=' + TOKEN + '; gitee_token=' + TOKEN
    }
)
resp = urllib.request.urlopen(req, context=ctx, timeout=15)
html = resp.read().decode('utf-8')

# Find all sidebar menu links
links = re.findall(r'href=[\'"]([^\'"]+settings[^\'"]*)[\'"][^>]*>([^<]+)</a>', html)
print('=== 设置页面菜单 ===')
for href, text in sorted(set(links)):
    text = text.strip()
    if text:
        print(f'  {text}: {href}')
        # Also check the linked page if it looks interesting
        if any(kw in text.lower() for kw in ['功能', 'page', '部署', '服务']):
            print(f'    -> 需要进一步检查')

# Count pages mentions
pages_count = html.lower().count('pages')
print(f'\n"pages" 出现次数: {pages_count}')
if pages_count > 0:
    for i, line in enumerate(html.split('\n')):
        if 'pages' in line.lower():
            print(f'  行{i}: {line.strip()[:150]}')

# Check feature settings specifically
if '功能设置' in html:
    print('\n✅ 功能设置 存在')
    # Try to access it
    req2 = urllib.request.Request(
        'https://gitee.com/wang7f/erjian-study/settings/features',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    try:
        resp2 = urllib.request.urlopen(req2, context=ctx, timeout=10)
        html2 = resp2.read().decode('utf-8')
        if 'pages' in html2.lower():
            print('  功能设置页面包含Pages')
            for line in html2.split('\n'):
                if 'pages' in line.lower():
                    print(f'    {line.strip()[:150]}')
        else:
            print('  功能设置页面不包含Pages')
    except:
        print('  无法访问功能设置页面')
