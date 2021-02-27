@echo off
IF Exist "shutdown" (
    del shutdown
)

:Start
IF Exist "shutdown" GOTO:exit
py run.py
GOTO:Start
:exit