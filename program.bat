@ECHO OFF
del /f fil
del /f bild.jpg
python getPic.py
:waitloop
IF EXIST "bild.jpg" GOTO waitloopend
timeout /t 1
goto waitloop
:waitloopend
start cmd /k helper.bat
:waitloop
IF EXIST "fil" GOTO waitloopend
timeout /t 3
goto waitloop
:waitloopend
taskkill /IM java.exe
python getCodes.py
pause