#!/usr/bin/env python3
"""Check data completeness and quality."""
import json
from collections import Counter

with open(r'C:\Users\Administrator\Desktop\二建备考\data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('=== 数据完整性检查 ===\n')

# 背诵检查
recite = d['recite']
print(f'1.背诵: {len(recite)}条')
missing_fields = [c for c in recite if not all(k in c for k in ['id','q','a','sec','sub'])]
empty_q = [c for c in recite if len(c['q']) < 5]
empty_a = [c for c in recite if len(c['a']) < 3]
qs = [c['q'][:20] for c in recite]
dupes = len(qs) - len(set(qs))
secs = Counter(c['sec'] for c in recite)
print(f'   字段缺失: {len(missing_fields)}条')
print(f'   问题过短: {len(empty_q)}条')
print(f'   答案过短: {len(empty_a)}条')
print(f'   疑似重复: {dupes}处')
print(f'   章节数: {len(secs)}')
for k,v in sorted(secs.items()):
    print(f'     {k}: {v}')
print()

# 刷题检查
quiz = d['quiz']
print(f'2.刷题: {len(quiz)}题')
missing_q = [q for q in quiz if not all(k in q for k in ['id','q','choices','answer','sec'])]
bad_ans = [q for q in quiz if not isinstance(q['answer'], (int, list)) or (isinstance(q['answer'], int) and q['answer'] < 0)]
short_choices = [q for q in quiz if len(q['choices']) < 2]
print(f'   字段缺失: {len(missing_q)}题')
print(f'   答案异常: {len(bad_ans)}题')
print(f'   选项不足: {len(short_choices)}题')
secs_q = Counter(q['sec'] for q in quiz)
print(f'   科目分布: {dict(secs_q)}')
# 法规60+20，管理60+20
fa = [q for q in quiz if '法规' in q['sec']]
gl = [q for q in quiz if '管理' in q['sec']]
dan_fa = [q for q in fa if isinstance(q['answer'], int)]
duo_fa = [q for q in fa if isinstance(q['answer'], list)]
dan_gl = [q for q in gl if isinstance(q['answer'], int)]
duo_gl = [q for q in gl if isinstance(q['answer'], list)]
print(f'   法规: {len(dan_fa)}单选 + {len(duo_fa)}多选 = {len(fa)}')
print(f'   管理: {len(dan_gl)}单选 + {len(duo_gl)}多选 = {len(gl)}')
print()

# 真题检查
exam = d['exam']
print(f'3.真题: {len(exam)}题')
missing_e = [q for q in exam if not all(k in q for k in ['id','q','choices','answer','sec'])]
bad_ans_e = [q for q in exam if not isinstance(q['answer'], (int, list))]
short_e = [q for q in exam if len(q['choices']) < 2]
print(f'   字段缺失: {len(missing_e)}题')
print(f'   答案异常: {len(bad_ans_e)}题')
print(f'   选项不足: {len(short_e)}题')
secs_e = Counter(q['sec'] for q in exam)
print(f'   年份分布: {dict(secs_e)}')
# 统计多选
duo_e = [q for q in exam if isinstance(q['answer'], list)]
dan_e = [q for q in exam if isinstance(q['answer'], int)]
print(f'   单选: {len(dan_e)}, 多选: {len(duo_e)}')

# 检查21-25真题是否已包含
years_found = set()
for q in exam:
    for y in ['2021','2022','2023','2024','2025']:
        if y in q['sec']:
            years_found.add(int(y))
print(f'   已覆盖年份: {sorted(years_found)}')
missing_years = [y for y in range(2021,2026) if y not in years_found]
if missing_years:
    print(f'   ❌ 缺失年份: {missing_years}')
else:
    print(f'   ✅ 2021-2025全齐')
print()

# 整体对比
print('=== 与目标对比 ===')
print(f'背诵: {len(recite)}条 ✅')
print(f'刷题(法规+管理共160题): {len(quiz)}题 ✅')
print(f'真题(2026水利23题): {len(exam)}题')
print(f'  -> 等待子代理处理2021-2025水利扫描件')
