#!/usr/bin/env python3
"""
合并桌面一建题库到 App DATA 格式
输入:questions_data.json(法规/经济/管理) + recite_cards.json(背诵) + index.html(现有真题/案例)
输出:yijian_full.json(供 merge_data.py 注入)
"""
import json, re, os
from pathlib import Path

BASE = Path('C:/Users/Administrator/Desktop')
HTML_PATH = Path('C:/Users/Administrator/Desktop/二建备考/index.html')

# 1. 读取 App 内嵌的 DATA(用于保留真题/案例)
html = HTML_PATH.read_text(encoding='utf-8')
m = re.search(r'window\.DATA\s*=\s*(\{[\s\S]+?\});', html)
if not m:
    # 大括号配平
    start = html.find('window.DATA = {')
    if start < 0:
        raise SystemExit('未找到 window.DATA')
    i = start
    depth = 0
    end = -1
    while i < len(html):
        if html[i] == '{':
            depth += 1
        elif html[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
        i += 1
    json_str = html[start + len('window.DATA = '):end]
else:
    json_str = m.group(1)
app_data = json.loads(json_str)
print(f'[App] recite={len(app_data["recite"])} quiz={len(app_data["quiz"])} exam={len(app_data["exam"])} case={len(app_data.get("case",[]))}')

# 2. 读取桌面 questions_data.json
qd = json.loads((BASE / '题库/questions_data.json').read_text(encoding='utf-8'))
print(f'[桌面] keys={list(qd.keys())}')

# 3. 转换 quiz 格式
def to_app_quiz(item, sec, idx_offset):
    """{id, type, question, options:{A..D}, answer:'D', analysis} → {id, q, choices, answer, analysis, sec}"""
    opts = item['options']
    choices = [opts.get(k, '') for k in ['A', 'B', 'C', 'D', 'E', 'F'] if opts.get(k)]
    if not choices:
        return None
    ans_letter = item['answer'].strip().upper()
    ans_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
    if ans_letter not in ans_map:
        return None
    ans_idx = ans_map[ans_letter]
    if ans_idx >= len(choices):
        return None
    # ID 前缀避免与原有 quiz 冲突
    new_id = f'y_{sec.replace("-", "_").replace("一建", "yj").lower()}_{idx_offset:04d}'
    return {
        'id': new_id,
        'q': item['question'],
        'choices': choices,
        'answer': ans_idx,
        'analysis': item.get('analysis', ''),
        'sec': sec
    }

# 收集桌面 quiz
new_quiz = []
for key, items in qd.items():
    for i, it in enumerate(items):
        app_q = to_app_quiz(it, key, i + 1)
        if app_q:
            new_quiz.append(app_q)

print(f'[转换] quiz {len(new_quiz)} 题')

# 4. 处理 App 内嵌的 quiz(法规80+管理80),避免重复
# App 内嵌 quiz 的 sec 是 "2026-法规" / "2026-管理",桌面 quiz 包含 2020-2025
# 合并策略:全量保留(用户可能想刷 2026 新题 + 历年真题)
app_quiz_2026 = [q for q in app_data['quiz'] if q.get('sec', '').startswith('2026-')]
print(f'[App 2026 quiz] {len(app_quiz_2026)} 题(法规80+管理80)')

# 5. 合并 quiz:桌面全部 + App 2026 部分
# 注意:App quiz id 是 q0001 这种,桌面新 id 是 y_*_,不冲突
all_quiz = new_quiz + app_quiz_2026
print(f'[合并 quiz] 总计 {len(all_quiz)} 题')

# 6. 读取 recite_cards.json
rc = json.loads((BASE / '题库/背书/recite_cards.json').read_text(encoding='utf-8'))
print(f'[桌面背诵] {len(rc)} 张')

# 检查 id 冲突
app_rc_ids = set(c['id'] for c in app_data['recite'])
desktop_rc_ids = set(c['id'] for c in rc)
overlap = app_rc_ids & desktop_rc_ids
print(f'[背诵 ID 重叠] {len(overlap)} 个')

# 合并策略:以桌面新版为准(更全)
# App 内嵌的 304 张 id 都在桌面 382 里(看下来 r0001-rxxxx 序号连续)
# 直接用桌面 382 张替换 App 内嵌 304 张
all_recite = rc
print(f'[合并 recite] {len(all_recite)} 张')

# 7. exam/case 保持 App 内嵌(都是水利真题/案例)
all_exam = app_data['exam']
all_case = app_data.get('case', [])

# 8. 组装最终 DATA
final = {
    'recite': all_recite,
    'quiz': all_quiz,
    'exam': all_exam,
    'case': all_case,
    'video': {
        'courses': [
            {
                'id': 'lv_water_case',
                'teacher': '吕桂军',
                'school': '中大网校',
                'title': '04·2026 案例专项班·水利',
                'priority': 1,
                'note': '老师指定的"04冲刺",每天 1-2 节',
                'items': [
                    {'sec': '施工组织与进度管理(一)', 'mp4': '01.1-施工组织与进度管理（一）.mp4', 'pdf': '讲义/01.1-施工组织与进度管理（一）.mp4.pdf', 'size_mb': 99, 'est_min': 45},
                    {'sec': '施工组织与进度管理(二)', 'mp4': '02.2-施工组织与进度管理（二）.mp4', 'pdf': '讲义/02.2-施工组织与进度管理（二）.mp4.pdf', 'size_mb': 82, 'est_min': 40},
                    {'sec': '施工组织与进度管理(三)', 'mp4': '03.3-施工组织与进度管理（三）.mp4', 'pdf': '讲义/03.3-施工组织与进度管理（三）.mp4.pdf', 'size_mb': 67, 'est_min': 35},
                    {'sec': '施工组织与进度管理(四)', 'mp4': '04.4-施工组织与进度管理（四）.mp4', 'pdf': '讲义/04.4-施工组织与进度管理（四）.mp4.pdf', 'size_mb': 68, 'est_min': 35},
                    {'sec': '合同管理', 'mp4': '05.5-合同管理.mp4', 'pdf': '讲义/05.5-合同管理.mp4.pdf', 'size_mb': 72, 'est_min': 40},
                    {'sec': '成本管理', 'mp4': '06.6-成本管理.mp4', 'pdf': '讲义/06.6-成本管理.mp4.pdf', 'size_mb': 85, 'est_min': 45},
                    {'sec': '安全管理', 'mp4': '07.7-安全管理.mp4', 'pdf': '讲义/07.7-安全管理.mp4.pdf', 'size_mb': 91, 'est_min': 50},
                    {'sec': '质量管理(一)', 'mp4': '08.8-质量管理（一）.mp4', 'pdf': '讲义/08.8-质量管理（一）.mp4.pdf', 'size_mb': 69, 'est_min': 35},
                    {'sec': '质量管理(二)', 'mp4': '09.9-质量管理（二）.mp4', 'pdf': '讲义/09.9-质量管理（二）.mp4.pdf', 'size_mb': 68, 'est_min': 35}
                ]
            },
            {
                'id': 'chenyin_fagui',
                'teacher': '陈印',
                'school': 'YL',
                'title': '11·2026 法规冲刺串讲班',
                'priority': 1,
                'note': '⭐推荐;25 节全听完时间不允许,只听⭐章节',
                'items': [{'sec': f'第{i:02d}节课', 'flv': f'{i:02d}.第{"0" if i<=11 else ""}{"1" if i>11 else "0"}节课.flv', 'pdf': 'WM_Removed_2026一建法规大V冲刺讲义627-28全【打印版】pdf.pdf', 'size_mb': 145, 'est_min': 40} for i in range(1, 24)] + [{'sec': '讲义(打印版)', 'pdf': 'WM_Removed_2026一建法规大V冲刺讲义627-28全【打印版】pdf.pdf', 'size_mb': 4, 'est_min': 0}]
            },
            {
                'id': 'qiulei_jingji',
                'teacher': '邱磊',
                'school': 'YL',
                'title': '11·2026 经济大V冲刺密训班',
                'priority': 1,
                'note': '⭐推荐;23 节,公式表是核心,先读讲义后听⭐',
                'items': [{'sec': f'第{i:02d}节课', 'flv': f'{i:02d}.第{"01" if i<=12 else "0"}{"1" if i<=12 else ""}节课.flv', 'size_mb': 280, 'est_min': 50} for i in range(1, 24)]
            },
            {
                'id': 'lina_guanli',
                'teacher': '李娜',
                'school': '面授内训',
                'title': '17·2026 管理面授内训班',
                'priority': 2,
                'note': '1.5G 单文件太重,先看讲义 PDF,看不懂再听对应片段',
                'items': [
                    {'sec': '完整课程', 'mp4': '李娜内训01-04.mp4', 'size_mb': 1500, 'est_min': 240},
                    {'sec': '内训讲义', 'pdf': 'WM_管理-李娜-内训讲义.pdf', 'size_mb': 76, 'est_min': 0},
                    {'sec': '内训试卷', 'pdf': 'WM_管理-李娜-内训试卷.pdf', 'size_mb': 13, 'est_min': 0}
                ]
            },
            {
                'id': 'liuerlin_water',
                'teacher': '刘二林',
                'school': '建工社',
                'title': '07·2026 强化提升直播·水利',
                'priority': 3,
                'note': 'HTML加密视频不能直接看,只看 PDF 讲义',
                'items': [
                    {'sec': '1.1 水利水电工程勘测', 'pdf': '讲义/01节1.1水利水电工程勘测（04.16）.pdf', 'size_mb': 6.1, 'est_min': 0},
                    {'sec': '1.2 水利水电工程设计', 'pdf': '讲义/02节1.2水利水电工程设计（04.16）.pdf', 'size_mb': 4.1, 'est_min': 0}
                ]
            }
        ]
    }
}

# 9. 输出
out_path = Path('C:/Users/Administrator/Desktop/二建备考/yijian_full.json')
out_path.write_text(json.dumps(final, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'[输出] {out_path} {out_path.stat().st_size/1024:.1f} KB')
print(f'[最终统计] recite {len(final["recite"])} | quiz {len(final["quiz"])} | exam {len(final["exam"])} | case {len(final["case"])} | video {len(final["video"]["courses"])} 课程/{sum(len(c["items"]) for c in final["video"]["courses"])} 节')
