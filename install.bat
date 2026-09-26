@echo off
setlocal EnableDelayedExpansion
title Starbound Korean Translation - One-click installer
cd /d "%~dp0"
set "SRC=%~dp0"
set "SB="
set "MODS="

echo ============================================================
echo  Starbound Korean Translation installer
echo  Installs: female_translation.pak, zz_female_overhaul.pak,
echo            gic_4_3_compat_fixes\
echo ============================================================
echo.

rem --- 1) a folder dropped on this .bat counts as the target ---
if not "%~1"=="" set "SB=%~1"

rem --- 2) default Steam location ---
if not defined SB if exist "C:\Program Files (x86)\Steam\steamapps\common\Starbound\assets\packed.pak" set "SB=C:\Program Files (x86)\Steam\steamapps\common\Starbound"

rem --- 3) Steam install path from registry ---
if not defined SB (
    for /f "usebackq delims=" %%P in (`powershell -NoProfile -Command "(Get-ItemProperty 'HKCU:\Software\Valve\Steam' -ErrorAction SilentlyContinue).SteamPath"`) do set "STEAM=%%P"
    if defined STEAM if exist "!STEAM!\steamapps\common\Starbound\assets\packed.pak" set "SB=!STEAM!\steamapps\common\Starbound"
)

rem --- 4) scan drives: <drive>:\steamapps, <drive>:\SteamLibrary\steamapps, <drive>:\<dir>\steamapps ---
if not defined SB (
    for %%D in (C D E F G H I J) do (
        if exist "%%D:\steamapps\common\Starbound\assets\packed.pak" set "SB=%%D:\steamapps\common\Starbound"
        if not defined SB if exist "%%D:\SteamLibrary\steamapps\common\Starbound\assets\packed.pak" set "SB=%%D:\SteamLibrary\steamapps\common\Starbound"
        if not defined SB (
            for /d %%L in ("%%D:\*") do (
                if not defined SB if exist "%%L\steamapps\common\Starbound\assets\packed.pak" set "SB=%%L\steamapps\common\Starbound"
            )
        )
    )
)

rem --- 5) ask the user ---
if not defined SB (
    echo Could not find Starbound automatically.
    set /p "SB=Enter the Starbound folder path (e.g. E:\My Games\steamapps\common\Starbound): "
)

rem --- normalize ---
set "SB=%SB:"=%"
if "%SB:~-1%"=="\" set "SB=%SB:~0,-1%"
if /i "%SB:~-4%"=="mods" (
    set "MODS=%SB%"
) else if exist "%SB%\mods" (
    set "MODS=%SB%\mods"
) else if exist "%SB%\assets\packed.pak" (
    mkdir "%SB%\mods" 2>nul
    set "MODS=%SB%\mods"
)

if not defined MODS (
    echo [ERROR] "%SB%" is not a valid Starbound folder.
    goto :fail
)

echo Target mods folder: %MODS%
echo.

set "FAILED=0"

if exist "%SRC%female_translation.pak" (
    copy /y "%SRC%female_translation.pak" "%MODS%\" >nul
    if errorlevel 1 (echo   [FAIL] female_translation.pak & set "FAILED=1") else echo   [OK] female_translation.pak
) else (
    echo   [SKIP] female_translation.pak - not found next to this installer
)

if exist "%SRC%zz_female_overhaul.pak" (
    copy /y "%SRC%zz_female_overhaul.pak" "%MODS%\" >nul
    if errorlevel 1 (echo   [FAIL] zz_female_overhaul.pak & set "FAILED=1") else echo   [OK] zz_female_overhaul.pak
) else (
    echo   [SKIP] zz_female_overhaul.pak - not found next to this installer
)

if exist "%SRC%gic_4_3_compat_fixes\_metadata" (
    xcopy /e /i /y /q "%SRC%gic_4_3_compat_fixes" "%MODS%\gic_4_3_compat_fixes" >nul
    if errorlevel 1 (echo   [FAIL] gic_4_3_compat_fixes & set "FAILED=1") else echo   [OK] gic_4_3_compat_fixes\
) else (
    echo   [SKIP] gic_4_3_compat_fixes - folder not found next to this installer
)

echo.
if "%FAILED%"=="1" (
    echo Finished with errors - see [FAIL] lines above.
) else (
    echo Done. Launch Starbound to play with the Korean translation.
)
pause
exit /b 0

:fail
echo.
echo You can also drag your Starbound folder onto this .bat file.
pause
exit /b 1
