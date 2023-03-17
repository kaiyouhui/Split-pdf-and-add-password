@echo off

rem Check if Chocolatey is installed
where choco > nul 2>&1
if errorlevel 1 (
    rem Chocolatey is not installed, install it
    powershell -Command "Start-Process cmd -Verb RunAs -ArgumentList '/c powershell -Command ""Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(''https://chocolatey.org/install.ps1''))""'"
)

rem Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    rem Python is not installed, install it with Chocolatey
    echo Python is not installed, installing now...
    choco install python3 -y
)

rem Check if PyPDF2 is installed
pip show PyPDF2 > nul 2>&1
if errorlevel 1 (
    rem PyPDF2 is not installed, install it with pip
    echo PyPDF2 is not installed, installing now...
    pip install PyPDF2==1.26.0
)

:: Run Python script
setlocal EnableDelayedExpansion
set "SCRIPT=split.py"
set "INPUT=paystubs.pdf"
set "OUTPUT=."
set "PASSWORD=password.csv"

cd /d %~dp0

python "%SCRIPT%" "%INPUT%" "%OUTPUT%" "%PASSWORD%"
