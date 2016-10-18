@echo off

call env\Scripts\activate
if %errorlevel% neq 0 goto error

python -m pip install --upgrade pip
if %errorlevel% neq 0 goto error

pip install --upgrade setuptools
if %errorlevel% neq 0 goto error

pip install PyQt5
if %errorlevel% neq 0 goto error

python setup.py install
if %errorlevel% neq 0 goto error

goto exit

:error
pause
exit

:exit