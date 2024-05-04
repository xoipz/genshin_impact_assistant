@echo off
:: 设置当前目录为批处理文件所在的目录
cd /d %~dp0

:: 运行 Python 脚本，使用相对路径指定 Python 解释器和脚本文件的位置
set PYTHONIOENCODING=utf8
call ..\venv\Scripts\python.exe ..\source\task\claim_reward\claim_reward.py