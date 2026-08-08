@echo off
chcp 65001 >nul
REM 二建备考App - 应用题库更新脚本
REM 用法: 双击运行(将以原子方式覆盖 index.html)

setlocal
cd /d "%~dp0"

if not exist "index.html.new" (
    echo ❌ 未找到 index.html.new
    echo    请先用 merge_data.py 生成更新包
    pause
    exit /b 1
)

echo 📦 发现 index.html.new
echo.

REM 备份当前
set TS=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TS=%TS: =0%
copy /Y "index.html" "index.html.backup_%TS%" >nul
echo ✓ 已备份到 index.html.backup_%TS%

REM 原子替换
move /Y "index.html.new" "index.html"
if errorlevel 1 (
    echo ❌ 替换失败,请确认没有程序占用 index.html (关闭编辑器/WPS等)
    pause
    exit /b 1
)

echo ✅ 已应用更新
echo.
echo 📤 推送部署 (可选):
echo    git add index.html
echo    git commit -m "更新题库"
echo    git push origin main
echo.
pause