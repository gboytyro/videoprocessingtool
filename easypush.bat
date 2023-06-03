@echo off
set /p commit_message=Enter commit message: 
git add --all
git commit -m "%commit_message%"
git push
pause