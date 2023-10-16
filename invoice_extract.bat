@echo off

:menu
cls
echo 1. Run the program
echo 2. Quit

set /p choice=Enter your choice (1 or 2): 

if "%choice%"=="1" (
    echo Running the program...
    C:\Users\Ramesh\Desktop\chatgpt_selenium\cs_env\Scripts\python.exe "C:\Users\Ramesh\Desktop\chatgpt_selenium\main.py"
    pause
    goto menu
) else if "%choice%"=="2" (
    echo Quitting...
    exit
) else (
    echo Invalid choice. Please enter 1 or 2.
    timeout /nobreak /t 2 >nul
    goto menu
)
