#!/usr/bin/env python3
"""Final merge of all data + update inline fallback."""
import json, re

# 1. Read all sources
with open(r'C:\Users\Administrator\Desktop\二建备考\data.json', 'r', encoding='utf-8') as f:
    app_data = json.load(f)

with open(r'C:\Users\Administrator\Desktop\题库\背书\recite_cards.json', 'r', encoding='utf-8') as f:
    new_cards = json.load(f)

# 2. Merge recite cards (deduplicate by first 30 chars of question)
existing_qs = set(c['q'][:30] for c in app_data['recite'])
added = 0
for c in new_cards:
    if c['q'][:30] not in existing_qs:
        existing_qs.add(c['q'][:30])
        app_data['recite'].append(c)
        added += 1

# Re-number
for i, c in enumerate(app_data['recite']):
    c['id'] = 'r{:04d}'.format(i+1)

print('背诵: 原{}条 + 新增{}条 = {}条'.format(
    len(app_data['recite']) - added, added, len(app_data['recite'])))
print('刷题: {}题'.format(len(app_data['quiz'])))
print('真题: {}题'.format(len(app_data['exam'])))
for q in app_data['quiz']:
    print('  {}: {}'.format(q['sec'], q['q'][:40]))
print()

# 3. Save updated data.json
with open(r'C:\Users\Administrator\Desktop\二建备考\data.json', 'w', encoding='utf-8') as f:
    json.dump(app_data, f, ensure_ascii=False, indent=2)

# 4. Update inline fallback in index.html
html_path = r'C:\Users\Administrator\Desktop\二建备考\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

inline_json = json.dumps(app_data, ensure_ascii=False)
html = re.sub(
    r"const INLINE_DATA = \{.*?\};",
    'const INLINE_DATA = ' + inline_json + ';',
    html,
    flags=re.DOTALL
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('内联数据更新: {}KB'.format(len(inline_json)//1024))

# Verify
if 'const INLINE_DATA = {' in html:
    print('✅ INLINE_DATA 验证通过')
else:
    print('❌ INLINE_DATA 缺失')

# Summary
print()
print('=== 最终数据汇总 ===')
print('背诵: {}条'.format(len(app_data['recite'])))
print('刷题: {}题'.format(len(app_data['quiz'])))
print('真题: {}题'.format(len(app_data['exam'])))
