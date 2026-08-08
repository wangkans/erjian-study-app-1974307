# 二建备考 App - WorkBuddy 接手说明

> 2026-07-27 由 Hermes 移交
> 用户同时使用 Hermes 和 WorkBuddy,经常协调两者。本文档供 WorkBuddy 单方面接手此项目。

---

## 一、项目一句话

单文件HTML的"二建备考题库App",部署在 Cloudflare Pages,用户鸿蒙手机浏览器打开刷题。

| 项 | 值 |
|---|---|
| **部署URL** | https://erjian-study-app-1974307.pages.dev |
| **GitHub仓库** | git@github.com:wangkans/erjian-study-app-1974307.git |
| **工作目录** | `C:\Users\Administrator\Desktop\二建备考\` |
| **截止日期** | 2026-08-07(剩11天) |
| **架构** | 单文件HTML(264K)+ 内嵌数据 + PWA + Cloudflare缓存 |

---

## 二、用户核心需求(不能再删的)

1. **背诵继续** - 304条知识点 + SM-2间隔重复 + 主动回忆 + 5秒倒计时 + 首字提示
2. **公共课错题过一遍** + **05习题班真题视频**
3. **实务21-25五年真题** + **26年三科真题**
4. **截止日期**: 2026-08-07

---

## 三、用户偏好(踩过的坑,WorkBuddy必须遵守)

### 沟通风格
- **短句直说**,给选项再执行,不绕弯
- **两道汇报口径**: 简洁版先给结论
- 需求不清时主动澄清,不要靠猜测执行
- **不要冗长铺垫** - 回答先给答案再解释原因

### 技术偏好
- **Excel**: 11pt微软雅黑,无底色无边框,仅标题加粗,2位小数,优先用原生公式(=ROUND/=SUM)
- **数据源优先级**: 原始收方单 > 计算表 > 汇总表
- **写xlsx前taskkill**强关et/wps/EXCEL进程

### 用户设备
- **鸿蒙手机**(华为浏览器/微信打开),**不装APP**
- 链接操作路径:"微信文件传输→复制→浏览器"很复杂
- **部署完任何web应用,第一优先级是给一个能记住的入口**(短链/可书签)

### 学习类App必备功能
- **冲刺(限时)模式**(10秒/题)
- **多选题**支持
- **错题复习**
- **互动答题**(AI出题→用户答→AI判对错+解析),**不要纯被动翻卡**
- 背诵卡要**口语化Q&A**,短句不犯困
- 记忆弱,需快速反复刷题强化

### 修复循环信号(关键!)
- 用户连续说"还是不行/请全面排查"=信号,增量修复不够
- "**重来**"=完全重建的直接指令
- 修复超3轮就**delete_rows全清重建**(不要补丁)

### 超时硬指令
- **任何进程/API/轮询 > 5分钟必须立即kill**
- 已踩坑:tradingagents-analysis跑ST中迪6+分钟未及时终止

### 工具陷阱
- **execute_code不保留跨调用import**,首次NameError:os就切terminal工具
- **vision读模糊数字易"教科书补全"幻觉**,必多源验证

---

## 四、App功能清单(已部署,不能再丢)

| 模块 | 功能 | 状态 |
|------|------|:----:|
| **背诵** | 304条知识点 + 乱序 + 主动回忆 + 5秒倒计时 + 智能判分 + 关键词高亮 + 历史复习次数 + 累计秒数 + 首字提示 | ✅ |
| **SM-2间隔重复** | 艾宾浩斯曲线(1→6→17→47→141天)+ EF/I/N 状态 + 复习质量分级 | ✅ |
| **刷题** | 160题(法规80+管理80)+ 多选支持 | ✅ |
| **真题** | 123题(2021-2025 100题 + 2026 23题)+ 解析 | ✅ |
| **案例题** | 10题 + 看题→自写答案→提交→对照自评 | ✅ |
| **冲刺** | 10秒/题,5题1轮,连对奖励 | ✅ |
| **模考** | 4种(法规/管理/水利选择/水利案例) | ✅ |
| **进度** | 4项进度条 + 30分钟背诵底线 + 今日目标动态计算 | ✅ |
| **激励** | 连续打卡 + 等级 + 10个成就 + 撒花庆祝 + 学习日历 | ✅ |
| **辅助** | 搜索 + 语音朗读 + 错题本 + 番茄钟 + 切换模式 + 收藏 | ✅ |
| **PWA** | 内联 manifest data URL + 添加到主屏幕 | ✅ |
| **深色模式** | 切换按钮 + localStorage记忆 | ✅ |

---

## 五、关键技术决策(WorkBuddy改任何东西前必读!)

| # | 决策 | 原因 |
|---|------|------|
| 1 | **数据内嵌到HTML** | 手机fetch外部JSON不可靠(改用同步XHR仍失败过) |
| 2 | **零IIFE架构** | 用户多次遭遇IIFE局部变量陷阱;所有函数直接全局 |
| 3 | **window.DATA 单独注入** | 必须先执行DATA脚本,再执行logic |
| 4 | **数据 script 在 logic script 之前** | 否则init()时DATA未就绪 |
| 5 | **禁用SW** | 比SW版本号升级更可靠,避免缓存陷阱 |
| 6 | **tryInit() 轮询** | 防止缓存导致空数据 |
| 7 | **panel用class切换**,不设`style="display:none"` | CSS class被内联style覆盖导致内容不可见 |
| 8 | **shuffleOn=true 默认** | 用户希望每次进入背诵tab自动乱序 |
| 9 | **updateDaily()必须放在rateR early-return之前** | 否则easy路径永远不更新进度 |
| 10 | **switchTab用data-tab属性** | textContent匹配"案例/模考"会重名 |
| 11 | **批量加HTML时JS+HTML一一对应** | 否则JS引用null元素 |
| 12 | **真实换行符转义为`\n`** | 否则截断JS字符串语法错误 |
| 13 | **node --check验证** | 每次部署前捕获JS语法错误 |
| 14 | **PWA用data URL** | Cloudflare把manifest.json当404 |
| 15 | **showHint首字公式** `firstChar + '...(' + w.length + '字)'` | 之前的占位符`安__`无意义 |
| 16 | **localStorage 跨设备失效** | 关电脑可访问App(CF Pages),但学习进度只在当前浏览器 |

---

## 六、已修复的关键Bug(WorkBuddy别再踩!)

| Bug | 根因 | 修复 |
|-----|------|------|
| 一键开始学习没反应 | `startAutoFlow` 未暴露到window | 暴露到window |
| 所有按钮没反应 | examMark中`参考答案:\r\n'`真实换行截断字符串 | 替换为`\n`转义 |
| "题库为空" | `DATA`在IIFE内是空对象 | 改为`window.DATA`(48处)|
| 背诵内容空白 | panel-recite内联`style="display:none"`覆盖CSS | 删除内联display:none |
| SW缓存旧版 | ejian-v1缓存旧HTML | SW版本ejian-v1→v2,并最终禁用SW |
| submitRecall崩溃 | `userWords`变量未定义 | 加`var userWords = userAnswer.replace(...)` |
| 背诵每次第一题 | `shuffleOn`默认false | 改为true + chkShuffle默认checked |
| pickSpeed崩溃 | speedQ未初始化时q为undefined | 加防御`if(!speedQ) return` |
| 提示按钮"安__"是占位符 | `w.charAt(0)+'_'+'_'` 是错的 | 改为`firstChar + '...(N字)'` |
| 5秒倒计时是摆设 | 只有文案,无逻辑 | 加setInterval真实倒计时 |
| 进度不更新 | `updateDaily()`在`if(easy) return`之后 | 移到early-return之前 |
| 重复函数定义 | rateR/getNextReview 出现2次 | 清理后只保留一处 |

---

## 七、SM-2 算法参考

```javascript
// q=回忆质量 (0-5): 5=完全记住, 4=记得, 3=困难但记得, 2=错, 1=错且熟悉, 0=完全忘
// EF=easiness factor (起始2.5, 范围≥1.3), I=interval (天), n=repetition
function sm2(grade, prev) {
  var q = grade === 'easy' ? 5 : (grade === 'ok' ? 4 : 2);
  var prevEF = (prev && prev.ef) || 2.5;
  var prevI = (prev && prev.i) || 0;
  var prevN = (prev && prev.n) || 0;
  var ef = prevEF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02));
  if (ef < 1.3) ef = 1.3;
  var n, i;
  if (q < 3) { n = 0; i = 1; } // 失败重置
  else {
    n = prevN + 1;
    if (n == 1) i = 1;
    else if (n == 2) i = 6;
    else i = Math.round(prevI * ef);
  }
  return { ef, i, n, nextDays: i };
}
// 调度表:1次记住=1天后,2次=6天后,3次=17天后,4次≈47天,5次≈141天
```

---

## 八、用户当前缺口(优先级排序)

1. **实务(水利)选择真题库为空** - 仅有法规/管理,模考第三项缺数据
2. **案例题仅10题**(偏少)
3. **PDF扫描版题库未转结构化**(桌面题库都是PDF)
4. **模板化重构未做** - 用户表示"暂时不改"(2026-07-27原话)

---

## 九、桌面题库目录

```
C:\Users\Administrator\Desktop\题库\二建各科真题\
├── 2026二建水利_原文.txt     ← 含4道2026案例题原文
├── 2026二建法规_原文.txt     ← 法规真题80题
├── 2026二建管理_原文.txt     ← 管理真题80题
├── exam_data_2021_2025.json  ← 100道2021-2025水利真题(带解析)
└── 二级管理真题(2021-2025).pdf  ← 扫描版PDF
```

---

## 十、部署流程(Git → Cloudflare Pages)

```bash
cd "C:/Users/Administrator/Desktop/二建备考/"
# 改完index.html后:
node --check <(sed -n '/<script>/,/<\/script>/p' index.html | head -200)  # 简单语法验证
git add -A
git commit -m "描述改动"
git push origin main
# Cloudflare Pages会自动部署,1-2分钟后生效
# 用户手机端可能需加 ?cb=timestamp 破缓存
```

---

## 十一、WorkBuddy 接手后的首要任务

1. **确认App可访问** - 让用户打开 https://erjian-study-app-1974307.pages.dev 验证是否正常
2. **询问当前状态** - 当前工作目录 + 用户是否需要继续改进哪部分
3. **保持现有功能** - 任何改动必须保留:SM-2算法/主动回忆/乱序/倒计时/进度
4. **避免重做基础功能** - 直接进入优先级缺口(水利选择/案例题扩充/PDF转题库)

---

## 十二、给WorkBuddy的额外提醒

- 用户使用 `git@github.com:wangkans/...` SSH推代码,**不要用HTTPS**(可能因网络问题失败)
- 用户偏好**国内Gitee Pages**,但Gitee需实名认证,临时用Cloudflare Pages
- 用户偏好**直接给结论和方案**,不要"我建议..."的客套话
- 用户经常**连续多轮指出同一个问题**,这时要**完全重建**,不要增量修
- 桌面可能有临时验证脚本(`hermes-verify*.py`等),**不要清理用户未确认的文件**

---

**文档结束。WorkBuddy读完此文件后可直接进入工作状态。**

如有疑问,优先询问用户而非猜测执行。