@echo off
REM Script d'arrêt pour Windows

echo ========================================
echo Arret de Synapse Chat
echo ========================================
echo.

docker-compose down

if %errorlevel% equ 0 (
    echo.
    echo [OK] Services arretes avec succes !
) else (
    echo.
    echo [ERREUR] Erreur lors de l'arret
)

echo.
pause
