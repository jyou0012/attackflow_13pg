@echo off
setlocal enabledelayedexpansion
cd "C:\Users\Jiayu You\OneDrive - University of Adelaide\7015\code\attack-flow-main\attack-flow-main"

for %%i in ("C:\Users\Jiayu You\OneDrive - University of Adelaide\7015\code\attackflow_13pg\attackflow_13pg\media\outputFile\\*.json") do ( 
    poetry run af validate "%%i"
    
    REM Derive the .mmd filename from the .json filename
    set mmd_file=%%~ni.mmd
    
    REM Convert the .json file to a .mmd file
    poetry run af mermaid "%%i" "C:\Users\Jiayu You\OneDrive - University of Adelaide\7015\code\attackflow_13pg\attackflow_13pg\media\outputFile\!mmd_file!"
        
    echo.
    
)

