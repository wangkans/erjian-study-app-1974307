#!/usr/bin/env python3
"""Check HTML/JS code quality."""
import re

with open(r'C:\Users\Administrator\Desktop\二建备考\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('=== HTML/JS代码检查 ===')

# Script完整性
scripts = re.findall(r'<script[^>]*>.*?</script>', html, re.DOTALL)
print(f'script标签数: {len(scripts)}')

# 标签闭合检查
for tag in ['div', 'button', 'span', 'h1', 'p', 'section', 'header']:
    opens = len(re.findall(f'<{tag}[^>]*>', html))
    closes = len(re.findall(f'</{tag}>', html))
    if opens != closes:
        print(f'  ⚠️ <{tag}>: {opens}开 {closes}闭')

print(f'  body闭合: {"</body>" in html}')
print(f'  html闭合: {"</html>" in html}')

# 关键功能检查
checks = {
    'localStorage保存': 'localStorage' in html,
    'fetch加载数据': 'fetch(' in html,
    'onclick事件': 'onclick=' in html,
    '触屏优化': 'touch-action' in html or 'user-scalable=no' in html,
    '移动端viewport': 'viewport' in html,
    '深色模式': 'prefers-color-scheme' in html,
    'Service Worker': 'serviceWorker' in html or 'sw.js' in html,
    'PWA支持': 'manifest' in html,
    '离线缓存': 'INLINE_DATA' in html,
    '错误处理': 'catch(' in html or 'try' in html,
}
print()
print('=== 功能检查 ===')
for name, ok in checks.items():
    print(f'  {"✅" if ok else "❌"} {name}')

# 潜在问题
print()
print('=== 潜在问题 ===')
# 控制台错误检测
console_errors = re.findall(r'console\.(error|warn)\(', html)
print(f'  console.error/warn: {len(console_errors)}处')

# 检查未定义变量
undefined_patterns = ['INLINE_RECITE', 'INLINE_QUIZ', 'INLINE_EXAM']
for p in undefined_patterns:
    if p in html:
        print(f'  ⚠️ 旧变量引用: {p}')

# 完整数据大小
inline_match = re.search(r'const INLINE_DATA = ({.*?});', html, re.DOTALL)
if inline_match:
    size = len(inline_match.group(1))
    print(f'  内联数据大小: {size//1024}KB')
    if size > 100000:
        print(f'  ⚠️ 内联数据过大({size//1024}KB)，建议仅作fallback')

# 多选题支持
if 'Array.isArray' in html:
    print('  ✅ 多选题支持: 有')
else:
    print('  ❌ 多选题支持: 无')
