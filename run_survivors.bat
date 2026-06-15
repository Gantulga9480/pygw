@echo off
for %%A in ("%~dp0.") do set "PARENT_DIR=%%~dpA"
set PYTHONPATH=%PARENT_DIR%
cd "%~dp0examples"
python -m survivors
pause