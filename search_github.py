#!/usr/bin/env python3
import urllib.request, json, ssl

ctx = ssl.create_default_context()
# Search for erjian/二建 related repos
queries = [
    '二级建造师 刷题',
    '中国建造师 考试',
    'exam-quiz-app html',
    'anki-like chinese exam',
]

seen = set()
for q in queries:
    url = f'https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&per_page=10'
    req = urllib.request.Request(url, headers={
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'HermesAgent'
    })
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=15)
        data = json.loads(resp.read())
        print(f'\n=== 搜索: {q} (共{data["total_count"]}条) ===')
        for r in data.get('items', []):
            if r['html_url'] in seen:
                continue
            seen.add(r['html_url'])
            desc = (r.get('description') or '无描述')[:60]
            lang = r.get('language') or '?'
            print(f"★{r['stargazers_count']:>4} | {r['name'][:30]:<30} | [{lang:<10}] | {desc:<60} | {r['html_url']}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        print(f'HTTP {e.code} for {q}: {body}')
    except Exception as e:
        print(f'Error for {q}: {e}')
