@echo off

call env\Scripts\activate
if %errorlevel% neq 0 goto error

python setup.py install
if %errorlevel% neq 0 goto error

goto exit

:error
pause
exit

:exit