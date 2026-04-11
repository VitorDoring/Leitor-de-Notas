@echo off
title Gerador de Executavel

cd /d "%~dp0"

echo ===============================
echo VERIFICANDO PYINSTALLER...
echo ===============================

python -m PyInstaller --version >nul 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller nao encontrado. Instalando...
    
    python -m pip install pyinstaller

    IF %ERRORLEVEL% NEQ 0 (
        echo.
        echo ERRO ao instalar PyInstaller.
        echo Verifique se o Python esta instalado corretamente.
        pause
        exit
    )
)

echo.
echo ===============================
echo GERANDO EXECUTAVEL...
echo ===============================

pyinstaller --clean --onefile --windowed --name "Leitor de Notas" --icon=icon.ico main.py

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO ao gerar o executavel!
    pause
    exit
)

:: Remove pasta build da pasta atual
if exist "%~dp0build" (
    rmdir /s /q "%~dp0build"
)

:: Remove arquivo .spec da pasta atual
if exist "%~dp0Leitor de Notas.spec" (
    del /q "%~dp0Leitor de Notas.spec"
)

echo.
echo FINALIZADO COM SUCESSO!
timeout /t 2 >nul
exit