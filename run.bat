@echo off
IF Exist "shutdown" (
    del shutdown
)

:Start
IF Exist "shutdown" GOTO:exit
py bot.py
GOTO:Start
:exit