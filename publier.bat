@echo off
chcp 65001 > nul
echo ========================================================
echo    PUBLICATION AUTOMATIQUE SUR ROULEMENT.BIZID.FR
echo ========================================================
echo.
echo [1/3] Enregistrement des modifications locales...
git add .
git commit -m "Mise a jour automatique (%date% %time%)"
echo.
echo [2/3] Envoi automatique vers GitHub Pages...
git push origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo [3/3] SUCCES ! Votre site https://roulement.bizid.fr est a jour !
) else (
    echo [!] Une erreur est survenue lors de l'envoi vers GitHub.
)
echo.
echo Appuyez sur une touche pour quitter...
pause > nul
