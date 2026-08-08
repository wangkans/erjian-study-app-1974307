# -*- coding: utf-8 -*-
"""
merge_data.py — JSON 题库 → index.html 注入器
================================================
用途: 把 JSON 文件的内容,merge 进 index.html 的 window.DATA 块
      可选追加或替换原数据,自动跑 JS 语法验证 + git commit + push

用法:
  python merge_data.py data.json                 # 默认追加(append)
  python merge_data.py data.json --replace       # 替换原 DATA
  python merge_data.py data.json --type recite   # 只处理 recite 字段
  python merge_data.py data.json --commit "新增20题背诵"
  python merge_data.py data.json --push          # 推送到 GitHub (CF Pages 自动部署)
"""
import os, sys, json, re, argparse, subprocess
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(ROOT, 'index.html')


def extract_data_block(html):
    """从 index.html 提取 window.DATA = {...} JSON 字符串"""
    m = re.search(r'window\.DATA\s*=\s*\{', html)
    if not m:
        raise RuntimeError('未找到 window.DATA 赋值语句')
    start = m.end() - 1  # 指向 '{'
    depth = 0
    end = -1
    for i in range(start, len(html)):
        ch = html[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end < 0:
        raise RuntimeError('window.DATA 块未找到匹配的 }')
    json_str = html[start:end]
    # 验证可解析
    try:
        return json.loads(json_str), start, end
    except json.JSONDecodeError as e:
        raise RuntimeError(f'原 window.DATA JSON 解析失败: {e}')


def load_input(path, only_type=None):
    """读取用户提供的 JSON"""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list):
        # 单类型列表,需要 --type 参数
        if not only_type:
            raise ValueError('输入是单列表格,必须指定 --type (recite/quiz/exam/case)')
        data = {only_type: data}
    elif only_type:
        # 字典但用户指定只处理某类型
        data = {only_type: data.get(only_type, [])}
    return data


def merge_data(orig, new, replace=False):
    """合并数据:
    replace=True: 新数据完全覆盖 orig 对应类型
    replace=False: 按 id 去重追加
    """
    result = {k: list(v) for k, v in orig.items()}
    summary = {}
    for key in ('recite', 'quiz', 'exam', 'case'):
        new_items = new.get(key, [])
        if not new_items:
            summary[key] = (len(result.get(key, [])), 0, 0)
            continue
        if replace:
            result[key] = new_items
            summary[key] = (len(new_items), 0, len(new_items))
        else:
            existing_ids = {x['id'] for x in result.get(key, []) if 'id' in x}
            added = 0
            dup = 0
            for item in new_items:
                if item.get('id') in existing_ids:
                    dup += 1
                    continue
                result[key].append(item)
                existing_ids.add(item.get('id'))
                added += 1
            summary[key] = (len(result[key]), added, dup)
    return result, summary


def validate_data(data):
    """数据完整性验证"""
    errors = []
    for q in data.get('quiz', []) + data.get('exam', []):
        if not q.get('choices') or len(q['choices']) < 2:
            errors.append(f'{q.get("id","?")} 选项数={len(q.get("choices",[]))}')
            continue
        ans = q.get('answer')
        if ans is None:
            errors.append(f'{q.get("id","?")} 缺答案')
            continue
        if isinstance(ans, list):
            for a in ans:
                if a < 0 or a >= len(q['choices']):
                    errors.append(f'{q.get("id","?")} 多选答案{a}越界')
        else:
            if ans < 0 or ans >= len(q['choices']):
                errors.append(f'{q.get("id","?")} 单选答案{ans}越界')
    for c in data.get('case', []):
        if not c.get('scenario'):
            errors.append(f'{c.get("id","?")} 缺 scenario')
        if not c.get('points'):
            errors.append(f'{c.get("id","?")} 缺 points')
    for r in data.get('recite', []):
        if not r.get('q') or not r.get('a'):
            errors.append(f'{r.get("id","?")} 缺 q 或 a')
    return errors


def validate_js_syntax(html):
    """提取所有 <script> 块,用 JS 引擎检查语法"""
    # 用 Node.js 检查
    import tempfile
    fd, tmp = tempfile.mkstemp(suffix='.js')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(html)
        # 简化:用 node -c 检查会失败因为是 HTML;我们提取 script 块
        blocks = re.findall(r'<script>([\s\S]*?)</script>', html)
        with open(tmp, 'w', encoding='utf-8') as f:
            for i, b in enumerate(blocks):
                f.write(f'// === block {i} ===\n{b}\n')
        result = subprocess.run(
            ['node', '--check', tmp],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return False, result.stderr or result.stdout
        return True, ''
    finally:
        try: os.unlink(tmp)
        except: pass


def replace_data_block(html, start, end, new_data):
    """把原 DATA 块替换为新数据"""
    new_json = json.dumps(new_data, ensure_ascii=False, separators=(',', ':'))
    return html[:start] + new_json + html[end:]


def run(cmd, cwd=None, check=True):
    """执行 shell 命令,输出实时显示"""
    print('  $ ' + ' '.join(cmd))
    return subprocess.run(cmd, cwd=cwd or ROOT, capture_output=True, text=True, check=check)


def main():
    ap = argparse.ArgumentParser(description='二建备考App JSON 题库注入器')
    ap.add_argument('json_file', help='输入 JSON 文件路径')
    ap.add_argument('--replace', action='store_true', help='替换原 DATA(默认追加)')
    ap.add_argument('--type', choices=['recite','quiz','exam','case'],
                    help='只处理指定类型字段')
    ap.add_argument('--commit', help='git commit 信息(不指定则不提交)')
    ap.add_argument('--push', action='store_true', help='git push 到 origin main')
    ap.add_argument('--no-backup', action='store_true', help='不生成备份')
    args = ap.parse_args()

    if not os.path.exists(args.json_file):
        print(f'❌ 文件不存在: {args.json_file}')
        sys.exit(1)
    if not os.path.exists(INDEX):
        print(f'❌ index.html 不存在: {INDEX}')
        sys.exit(1)

    print(f'📖 读取 {args.json_file}')
    new_data = load_input(args.json_file, args.type)

    with open(INDEX, 'r', encoding='utf-8') as f:
        html = f.read()
    print(f'📖 解析 {INDEX}')
    orig_data, start, end = extract_data_block(html)
    print(f'  原 DATA: recite {len(orig_data.get("recite",[]))} | '
          f'quiz {len(orig_data.get("quiz",[]))} | '
          f'exam {len(orig_data.get("exam",[]))} | '
          f'case {len(orig_data.get("case",[]))}')

    print('🔀 合并数据...')
    merged, summary = merge_data(orig_data, new_data, args.replace)
    for k, (now, added, dup) in summary.items():
        if added > 0 or dup > 0:
            print(f'  {k}: 现 {now} 条 (新增 {added} / 重复跳过 {dup})')

    print('✓ 数据完整性验证...')
    errs = validate_data(merged)
    if errs:
        print(f'❌ 数据有 {len(errs)} 个问题:')
        for e in errs[:10]:
            print(f'  - {e}')
        ans = input('继续注入? (y/N): ')
        if ans.strip().lower() != 'y':
            print('已取消')
            return

    # 备份
    if not args.no_backup:
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup = INDEX + f'.backup_{ts}'
        with open(backup, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'📦 备份: {backup}')

    # 替换
    print('✏️  替换 window.DATA 块...')
    new_html = replace_data_block(html, start, end, merged)

    # 验证 JS 语法
    print('✓ JS 语法验证...')
    ok, err = validate_js_syntax(new_html)
    if not ok:
        print(f'❌ JS 语法错误:\n{err}')
        ans = input('是否仍要写入? 这可能导致App崩溃 (y/N): ')
        if ans.strip().lower() != 'y':
            print('已取消')
            return

    # 写入 - 用 .new 文件 + bat 脚本(避免被 WorkBuddy 等进程锁住的 index.html)
    new_path = INDEX + '.new'
    with open(new_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'✅ 已写入 {new_path}')

    # git
    if args.commit:
        print('📤 git commit...')
        # git add .new 暂存;真正提交要等用户运行 .bat
        run(['git', 'add', 'index.html.new'])
        run(['git', 'commit', '-m', args.commit + ' [pending apply]'])
    if args.push:
        print('📤 git push...')
        run(['git', 'push', 'origin', 'main'])

    print()
    print('🎉 完成!')
    print(f'  新数据: recite {len(merged["recite"])} | quiz {len(merged["quiz"])} | '
          f'exam {len(merged["exam"])} | case {len(merged["case"])}')
    print()
    print('⚠️  index.html 已被其他进程锁定(WorkBuddy 监控)')
    print(f'  1. 关闭可能占用 index.html 的程序(浏览器/WPS/编辑器等)')
    print(f'  2. 双击运行 apply_data_update.bat 应用更新')
    print(f'  3. 或者直接 git pull / git reset 获取最新版本')
    if not args.push:
        print('  提示: 加 --push 参数自动推送到 GitHub 触发 CF Pages 部署')


if __name__ == '__main__':
    main()