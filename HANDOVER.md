# 二建备考App 交接文档

> 新对话开始时，请先读取此文件了解项目全貌。
> 最后更新：2026-07-27

---

## 一、项目基本信息

| 项 | 值 |
|---|---|
| **项目名** | 二建备考题库学习App |
| **部署URL** | https://erjian-study-app-1974307.pages.dev |
| **GitHub仓库** | git@github.com:wangkans/erjian-study-app-1974307.git |
| **工作目录** | `C:\Users\Administrator\Desktop\二建备考\` |
| **架构** | 单文件HTML（index.html）+ PWA + 内嵌数据 |
| **部署平台** | Cloudflare Pages（GitHub推送自动部署） |
| **域名解析** | Cloudflare CDN（偶发返回旧版缓存，需`?cb=timestamp`刷） |

---

## 二、用户核心需求

1. **背诵继续** + **公共课错题过一遍 + 05习题班真题视频**
2. **实务21-25五年真题** + **26年三科真题**
3. **截止日期**：2026-08-07（剩余约10-11天，2026-07-27算起）

---

## 三、用户偏好（重要！必须遵守）

| 偏好 | 说明 |
|------|------|
| **沟通风格** | 短句直说，给选项再执行，不绕弯子 |
| **汇报口径** | 两道汇报（简洁版先给结论） |
| **数据源优先级** | 原始收方单 > 计算表 > 汇总表；不看文件名判断内容 |
| **Excel公式** | 用原生公式（=ROUND/=SUM），不写死静态值 |
| **Excel格式** | 11pt微软雅黑，无底色无边框，仅标题加粗，2位小数 |
| **数据判定** | 源文件=0的项标注 |
| **进度跟踪** | 4项进度条（背诵/刷题/真题/案例）+ 30分钟底线 |
| **纠错信号** | 用户连续说"不行/请全面排查"=信号，"重来"=完全重建 |
| **超时硬指令** | 任何进程/API/轮询 > 5分钟必须立即kill |
| **沙箱陷阱** | execute_code不保留import，首次NameError切terminal |
| **vision陷阱** | 模糊数字易"教科书补全"幻觉，多源验证 |

---

## 四、用户设备与环境

| 项 | 值 |
|---|---|
| **设备** | Windows 10 + 鸿蒙手机（华为浏览器/微信打开） |
| **链接访问路径** | 微信文件传输→复制→浏览器 |
| **GitHub用户名** | wangkans |
| **Cloudflare邮箱** | 547714027@qq.com |
| **学习截止** | 2026-08-07 |
| **做题位置** | 单文件HTML+数据内嵌（手机fetch外部JSON不可靠）|
| **额外AI** | 同时使用WorkBuddy |

---

## 五、App功能清单（已部署）

| 模块 | 功能 | 状态 |
|------|------|:----:|
| **背诵** | 304条知识点 + 乱序 + 主动回忆 + 5秒倒计时 + 智能判分 + 关键词高亮 + 历史复习次数 + 累计秒数 + 真首字提示 | ✅ |
| **SM-2间隔重复** | 艾宾浩斯曲线算法（1→6→17→47→141天）+ EF/I/N 状态 + 复习质量分级 | ✅ |
| **刷题** | 160题（法规80+管理80）+ 多选支持 + 单选+多选混合 | ✅ |
| **真题** | 223题（2021-2025 100题 + 2026 23题 + 其他100题）+ 解析 | ✅ |
| **案例题** | 10题（2021-2025+2026真题）+ 看题→自写答案→提交→对照自评→自动判分关键词 | ✅ |
| **冲刺** | 10秒/题，5题1轮，连对奖励 | ✅ |
| **模考** | 4种考试（法规80题120min/管理80题120min/水利选择30题60min/水利案例4题80min）| ✅ |
| **进度** | 4项进度条 + 30分钟背诵底线 + 今日目标动态计算 | ✅ |
| **激励** | 连续打卡 + 等级系统 + 10个成就徽章 + 撒花庆祝 + 学习日历 | ✅ |
| **辅助** | 搜索 + 语音朗读 + 错题本 + 番茄钟 + 切换模式 + 收藏 | ✅ |
| **PWA** | 内联 manifest data URL + Service Worker + 添加到主屏幕 | ✅ |
| **深色模式** | 切换按钮 + localStorage记忆 | ✅ |

---

## 六、关键技术决策（避免重犯）

| # | 决策 | 原因 |
|---|------|------|
| 1 | **数据内嵌到HTML** | 手机fetch外部JSON不可靠 |
| 2 | **零IIFE架构** | 用户多次遭遇IIFE局部变量陷阱；所有函数直接全局 |
| 3 | **window.DATA 单独注入** | 必须先执行DATA脚本，再执行logic |
| 4 | **数据 script 在 logic script 之前** | 否则init()时DATA未就绪 |
| 5 | **SW缓存版本ejian-v1→v2** | 用户旧缓存导致看到的是旧HTML |
| 6 | **禁用SW注册** | 彻底避免缓存问题，每次拿新版 |
| 7 | **tryInit() 轮询** | 防止缓存导致空数据 |
| 8 | **panel用class切换，不设style="display:none"** | CSS class被内联style覆盖导致内容不可见 |
| 9 | **shuffleOn=true 默认** | 用户希望每次进入背诵tab自动乱序 |
| 10 | **updateDaily() 必须放在rateR early-return之前** | 否则easy路径永远不更新进度 |
| 11 | **switchTab用data-tab属性** | textContent匹配"案例/模考"会重名 |
| 12 | **批量加HTML时JS+HTML一一对应** | 否则JS引用null元素 |
| 13 | **真实换行符转义为\\n** | 否则截断JS字符串语法错误 |
| 14 | **node --check验证** | 每次部署前捕获JS语法错误 |
| 15 | **PWA用data URL** | Cloudflare把manifest.json当404 |
| 16 | **showHint首字公式 `firstChar + '...(' + w.length + '字)'`** | 之前的占位符`安__`无意义 |
| 17 | **localStorage 跨设备失效** | 关电脑可访问App（CF Pages），但学习进度只在当前浏览器 |

---

## 七、已修复的关键Bug（保留供查询）

| Bug | 根因 | 修复 |
|-----|------|------|
| 一键开始学习没反应 | `startAutoFlow` 未暴露到window | 暴露到window |
| 所有按钮没反应 | examMark中`参考答案:\r\n'`真实换行截断字符串 | 替换为`\n`转义 |
| "题库为空" | `DATA`在IIFE内是空对象 | 改为`window.DATA`（48处）|
| 背诵内容空白 | panel-recite内联`style="display:none"`覆盖CSS | 删除内联display:none |
| SW缓存旧版 | ejian-v1缓存旧HTML | SW版本ejian-v1→v2，并最终禁用SW |
| submitRecall崩溃 | `userWords`变量未定义 | 加`var userWords = userAnswer.replace(...)` |
| 背诵每次第一题 | `shuffleOn`默认false | 改为true + chkShuffle默认checked |
| pickSpeed崩溃 | speedQ未初始化时q为undefined | 加防御`if(!speedQ) return` |
| 提示按钮"安__"是占位符 | `w.charAt(0)+'_'+'_'` 是错的 | 改为`firstChar + '...(N字)'` |
| 5秒倒计时是摆设 | 只有文案，无逻辑 | 加setInterval真实倒计时 |
| 进度不更新 | `updateDaily()`在`if(easy) return`之后 | 移到early-return之前 |
| 重复函数定义 | rateR/getNextReview 出现2次 | 清理后只保留一处 |

---

## 八、验证脚本位置

```
C:\Users\Administrator\AppData\Local\Temp\hermes-verify.py    ← 总验证
C:\Users\Administrator\AppData\Local\Temp\hermes-verify-sm2.py  ← SM-2验证
C:\Users\Administrator\AppData\Local\Temp\hermes-verify-sm2v2.py ← SM-2 v2
```

运行验证：
```bash
python3 "C:\Users\Administrator\AppData\Local\Temp\hermes-verify.py"
```

---

## 九、临时文件清理

```bash
# 清理由验证脚本创建的临时文件
cd C:/Users/Administrator/AppData/Local/Temp/
rm -f hermes-verify-*.py hermes-verify-*.js hermes-verify-*.html
```

---

## 十、当前待办

之前用户8项需求：
1. 美观界面 ✅
2. 时间倒计时 ✅
3. 题库准确性 ⚠️（quiz仅法规管理，缺实务水利选择）
4. 做题紧迫感 ✅（冲刺+模考）
5. 背诵效率 ✅（SM-2+主动回忆）
6. 真题 ✅
7. 案例题 ⚠️（10题，数量偏少）
8. 时间倒排完成度 ✅（4项进度条）

补充8项：错题本/学习数据分析/截图分享/错题解析/收藏夹/学习日历热力图/搜题/夜间模式

**用户最新选择**：A选项（1+2+3+4改进）+ **艾宾浩斯SM-2真实算法** — **已实施**

**用户提过但未实施的诉求**：
- **模板化** — 把App做成可复用题库模板，方便换题库
- **PDF转题库** — 用户桌面题库大多是PDF扫描版，需PDF→JSON工具

---

## 十一、Git关键提交历史

```
363b183 背诵升级: 艾宾浩斯SM-2算法+历史记录+首字提示+关键词高亮+停留秒数
6ddf46a 背诵体验升级: 5秒真倒计时+真首字提示+进度立即刷新+关电脑可访问
dfceed6 关键Bug修复: submitRecall 缺少 userWords 变量定义
1dd09b9 背诵: 默认开启乱序
347c781 Bug修复: pickSpeed加空数据防御
fa9be8a Bug修复: simPick/simNav/simSubmit 加空数据防御
57b0498 关键Bug修复: rateR 重复if+recall变量未定义
5035f94 Bug修复: submitMulti/submitMultiE 改用ansArr
70a26a8 Bug修复: submitMulti/submitMultiE 支持answer为数字/数组
```

---

## 十二、新对话接收时的首要任务

1. **确认App可访问** — 让用户打开 https://erjian-study-app-1974307.pages.dev 验证是否正常
2. **询问当前状态** — 当前工作目录 + 用户是否需要继续改进哪部分
3. **保持现有功能** — 任何改动必须保留：SM-2算法/主动回忆/乱序/倒计时/进度
4. **避免重做基础功能** — 直接进入**模板化重构**或**PDF转题库**方向

---

## 十三、当前关键文件结构

```
C:\Users\Administrator\Desktop\二建备考\
├── index.html          ← 主应用（~265KB，含全部JS/CSS/数据）
├── sw.js               ← Service Worker（已禁用但保留）
├── manifest.json       ← PWA清单（已内联到HTML）
├── HANDOVER.md         ← 本文件
└── (其他临时/验证脚本)

C:\Users\Administrator\Desktop\题库\二建各科真题\
├── 2026二建水利_原文.txt     ← 含4道2026案例题原文
├── 2026二建法规_原文.txt     ← 法规真题80题
├── 2026二建管理_原文.txt     ← 管理真题80题
├── exam_data_2021_2025.json  ← 100道2021-2025水利真题（带解析）
└── 二级管理真题(2021-2025).pdf  ← 扫描版PDF
```

---

## 十四、SM-2 间隔重复算法参考

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

// 调度表：1次记住=1天后，2次=6天后，3次=17天后，4次≈47天，5次≈141天
```

---

**文档结束。新对话读取后可直接进入工作状态。**