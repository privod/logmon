@echo off

call env\Scripts\activate
if %errorlevel% neq 0 goto error

logmon-start.exe
if %errorlevel% neq 0 goto error

goto exit

:error
pause
exit

:exit