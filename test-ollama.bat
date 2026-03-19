@echo off
REM Script de test de connexion à Ollama distant

echo ========================================
echo Test de Connexion Ollama
echo ========================================
echo.

echo Test de connexion a : http://localhost:11434
echo.

REM Test avec curl (si disponible)
where curl >nul 2>&1
if %errorlevel% equ 0 (
    echo Test 1 : Liste des modeles disponibles
    echo.
    curl -s http://localhost:11434/api/tags
    echo.
    echo.
    
    echo Test 2 : Verification que Mistral est installe
    echo.
    curl -s http://localhost:11434/api/tags | findstr "mistral"
    if %errorlevel% equ 0 (
        echo.
        echo [OK] Mistral est bien installe sur Ollama !
    ) else (
        echo.
        echo [ATTENTION] Mistral ne semble pas etre installe
        echo.
        echo Pour l'installer, connectez-vous a votre VM et executez :
        echo   ollama pull mistral
    )
) else (
    echo Curl n'est pas disponible.
    echo.
    echo Testez manuellement dans votre navigateur :
    echo   http://localhost:11434/api/tags
    echo.
    echo Vous devriez voir une liste de modeles incluant "mistral"
)

echo.
echo ========================================
echo Test termine
echo ========================================
echo.
pause
