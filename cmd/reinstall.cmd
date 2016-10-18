@echo off

call :delete env
call :delete build
call :delete dist
call :delete logmon.egg-info

echo ������ ����� ����㠫쭮� ���থ��� "env" ...
python35 -m venv env
if %errorlevel% neq 0 goto error

call install.cmd
goto exit

:error
pause
exit

:delete
if exist %1 (
  echo ������ ����� "%1" ...
  rmdir %1 /S /Q
)

:exit