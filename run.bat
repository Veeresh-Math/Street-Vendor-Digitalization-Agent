@echo off
chcp 65001 >nul

echo.
echo  ============================================
echo   Street Vendor Digitalization Agent
echo   AICTE-IBM SkillsBuild Internship 2026
echo   Problem Statement No. 29
echo  ============================================
echo.
echo  Models:
echo    Generation : ibm/granite-4-h-small
echo    Embeddings : ibm/granite-embedding-278m-multilingual
echo.

:: Kill any process already using port 8000
echo  [INFO] Freeing port 8000 if occupied...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000 " 2^>nul') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo  Starting FastAPI server on http://localhost:8000
echo  Press Ctrl+C to stop.
echo.

python -m uvicorn backend.main:app --reload --port 8000 --host 127.0.0.1

pause
