@echo off
cd /d "C:\Users\win\Desktop\AI biligual bot"
"C:\Users\win\AppData\Local\Programs\Python\Python315\python.exe" main.py
if errorlevel 1 (
    exit /b 1
)
git add .
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "daily: auto generate daily report"
    git push
)
