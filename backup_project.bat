@echo off
setlocal
cd /d "%~dp0"

for /f "tokens=1-4 delims=/ " %%a in ("%date%") do (
    set DD=%%a
    set MM=%%b
    set YYYY=%%c
)
for /f "tokens=1-3 delims=:., " %%a in ("%time%") do (
    set HH=%%a
    set MN=%%b
    set SS=%%c
)
set HH=%HH: =0%
set ZIPNAME=backup\EVUS_ThiDua_%YYYY%%MM%%DD%_%HH%%MN%%SS%.zip

powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path '.streamlit','app','assets','config','data','docs','logs','tests','app.py','README.md','requirements.txt','.gitignore','run_local.bat','backup_project.bat' -DestinationPath '%ZIPNAME%' -Force"

echo Backup created: %ZIPNAME%
pause
