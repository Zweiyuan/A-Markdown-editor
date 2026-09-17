@echo off
setlocal
set "APP=%~dp0mdedit.exe"
if not exist "%APP%" (
  echo mdedit.exe not found.
  pause
  exit /b 1
)

reg add "HKCU\Software\Classes\mdedit.Markdown" /ve /d "Markdown Document" /f >nul
reg add "HKCU\Software\Classes\mdedit.Markdown\shell\open\command" /ve /d "\"%APP%\" \"%%1\"" /f >nul
reg add "HKCU\Software\Classes\Applications\mdedit.exe\shell\open\command" /ve /d "\"%APP%\" \"%%1\"" /f >nul
reg add "HKCU\Software\Classes\Applications\mdedit.exe\SupportedTypes" /v ".md" /t REG_SZ /d "" /f >nul
reg add "HKCU\Software\Classes\Applications\mdedit.exe\SupportedTypes" /v ".markdown" /t REG_SZ /d "" /f >nul
reg add "HKCU\Software\Classes\.md" /ve /d "mdedit.Markdown" /f >nul
reg add "HKCU\Software\Classes\.md\OpenWithProgids" /v "mdedit.Markdown" /t REG_NONE /f >nul
reg add "HKCU\Software\Classes\.markdown" /ve /d "mdedit.Markdown" /f >nul
reg add "HKCU\Software\Classes\.markdown\OpenWithProgids" /v "mdedit.Markdown" /t REG_NONE /f >nul
echo mdedit is registered for .md and .markdown files.
echo If Windows keeps another default app, use Open with and select mdedit once.
pause