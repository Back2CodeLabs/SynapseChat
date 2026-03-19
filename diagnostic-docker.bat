@echo off
REM Script de diagnostic Docker pour Windows

echo ========================================
echo Diagnostic Docker
echo ========================================
echo.

echo [1/5] Version Docker...
docker version
echo.

echo [2/5] Informations Docker...
docker info | findstr "CPUs Memory"
echo.

echo [3/5] Espace disque Docker...
docker system df
echo.

echo [4/5] Conteneurs en cours...
docker ps -a
echo.

echo [5/5] Test connexion Ollama...
curl -s http://localhost:11434/api/tags
echo.

echo ========================================
echo Diagnostic termine
echo ========================================
echo.
echo Recommandations :
echo.
echo 1. RAM Docker : minimum 4 GB, recommande 6-8 GB
echo 2. Espace disque : minimum 10 GB disponible
echo 3. CPU : minimum 2 coeurs
echo.
echo Pour augmenter les ressources :
echo   Docker Desktop ^> Settings ^> Resources
echo.
pause
